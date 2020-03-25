#!/usr/bin/env python
# ASCii VMSS Console - The power is in the terminal...

"""
Copyright (c) 2016, Marcelo Leal
Copyright (c) 2013, Tyler Hobbs
Description: The power is in the terminal...
License: MIT (see LICENSE.txt file for details)
"""
import os
import io
import struct
import threading
import time
from unicurses import *
from windows import *

def _seek_to_n_lines_from_end_ng(f, numlines=10):
	"""
	(Python3) Seek to `numlines` lines from the end of the file `f`.
	"""
	line_count = 0;

	for line in f:
		line_count += 1;
	pos = line_count - numlines;
	if (pos >= 0):
		f.seek(pos, 0);
	else:
		f.seek(0, 0);

def _seek_to_n_lines_from_end(f, numlines=10):
	"""
	Seek to `numlines` lines from the end of the file `f`.
	"""
	buf = ""
	buf_pos = 0
	f.seek(0, 2)  # seek to the end of the file
	line_count = 0

	while line_count < numlines:
		newline_pos = buf.rfind("\n", 0, buf_pos)
		file_pos = f.tell()

		if newline_pos == -1:
			if file_pos == 0:
				# start of file
				break
			else:
				toread = min(1024, file_pos)
				f.seek(-toread, 1)
				buf = f.read(toread) + buf[:buf_pos]
				f.seek(-toread, 1)
				buf_pos = len(buf) - 1
		else:
			# found a line
			buf_pos = newline_pos
			line_count += 1

	if line_count == numlines:
		f.seek(buf_pos + 1, 1)

def tail(filename, run_event, starting_lines=10):
	"""
	A generator for reading new lines off of the end of a file.  To start with,
	the last `starting_lines` lines will be read from the end.
	"""
	f = open(filename)
	current_size = os.stat(filename).st_size
	#There is no seek from the end of text files in Python 3...
	cur_version = sys.version_info;
	if (cur_version.major == 2):
		_seek_to_n_lines_from_end(f, starting_lines)
	else:
		_seek_to_n_lines_from_end_ng(f, starting_lines)
		#f.seek(0, 2);

	#Main tail loop...
	while (run_event.is_set()):
		new_size = os.stat(filename).st_size

		where = f.tell()
		line = f.readline()
		if not line:
			if new_size < current_size:
				# the file was probably truncated, reopen
				f = open(filename)
				current_size = new_size
				dashes = "-" * 20
				yield "\n"
				yield "\n"
				yield "%s file was truncated %s" % (dashes, dashes)
				yield "\n"
				yield "\n"
				time.sleep(0.25)
			else:
				time.sleep(0.25)
				f.seek(where)
		else:
			current_size = new_size
			yield line


def tail_in_window(filename, window, panel, run_event):
	"""
	Update a curses window with tailed lines from a file.
	"""
	lock = threading.Lock()
	title = " LOG ";
	max_lines, max_chars = getmaxyx(window)
	max_line_len = max_chars - 2
	wmove(window, 1, 0)

	for line in tail(filename, run_event, max_lines - 3):
		if len(line) > max_line_len:
			first_portion = line[0:max_line_len - 1] + "\n"
			trailing_len = max_line_len - (len("> ") + 1)
			remaining = ["> " + line[i:i + trailing_len] + "\n"
				for i in range(max_line_len - 1, len(line), trailing_len)]
			remaining[-1] = remaining[-1][0:-1]
			line_portions = [first_portion] + remaining
		else:
			line_portions = [line]

		for line_portion in line_portions:
			with lock:
				try:
					y, x = getyx(window)
					if y >= max_lines - 1:
						wmove(window, 1, 1)
						wdeleteln(window)
						wmove(window, y - 1, 1)
						wdeleteln(window)
						waddstr(window, line_portion)
					else:
						wmove(window, y, x + 1)
						waddstr(window, line_portion)

					#We save the cursor position, write the title, and put the cursor back in curse...
					y, x = getyx(window)
					box(window)
					write_str_color(window, 0, 5, title, 3, 0);
					wmove(window, y, x)
					#y, x = getyx(window)
					#wmove(window, y, x)

					if not (panel_hidden(panel)):
						#wrefresh(window)
						update_panels();
						#doupdate();
				#except KeyboardInterrupt:
				except:
					print("PROBLEM");

def _terminal_size():
	raw = fcntl.ioctl(0, termios.TIOCGWINSZ, struct.pack('HHHH', 0, 0, 0, 0))
	h, w, hp, wp = struct.unpack('HHHH', raw) 
	return w, h
