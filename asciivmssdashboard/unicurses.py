# UniCurses -- A unified multiplatform Curses provider library for Python 2.x/3.x
# Copyright (C) 2010 by Michael Kamensky.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

# import Curses (either natively if supported or via PDCurses using FFI if on MS Windows)
import sys
import os
import locale
import platform
global pdlib
global NCURSES
global PDC_LEAVEOK
global pdlib

PDC_LEAVEOK = False       # LeaveOK emulation in PDC
NCURSES = False           # Native curses support
NCURSES_AVAILABLE = False # True if the NCurses is available natively
pdlib = None              # PD library, if applicable
UCS_DEFAULT_WRAPPER = ""  # A constant for the default wrapper (ucs_reconfigure)
stdscr = -1               # A pointer to the standard screen

locale.setlocale(locale.LC_ALL,'')
code = locale.getpreferredencoding()   # TODO: fix this to actually work on native ncurses

try:
    import ctypes
except ImportError:
    print("Fatal error: this Python release does not support ctypes, please upgrade your Python distribution if you want to use UniCurses on a "+sys.platform+" platform.\n")
    raise ImportError("UniCurses initialization error - ctypes FFI not supported.")

try:
    import curses   # see if the platform supports curses natively 
    import curses.panel
    NCURSES_AVAILABLE = True
    NCURSES = True
except ImportError:
    if sys.platform.find('win') == -1: 
        print("Fatal error: this platform is not supported by UniCurses (either you're running a very old Python distribution below v2.6, or you're using an exotic operating system that's neither Win nor *nix).\n")
        raise ImportError("UniCurses initialization error - unsupported platform.")
    else:
        if (platform.architecture()[0] == "32bit"):
            pdcurses = "pdc34dll/pdcurses32.dll"
        else:
            pdcurses = "pdc34dll/pdcurses64.dll"

        current_dir = os.path.dirname(os.path.realpath(__file__))
        path_to_pdcurses = current_dir + "/" + pdcurses
        #print("Expecting pdcurses at: " + path_to_pdcurses)
        if not (os.access(pdcurses, os.F_OK) or os.access(path_to_pdcurses, os.F_OK)):
            print("Fatal error: can't find " + pdcurses + " for linking, make sure PDCurses v3.4+ is in the same folder as UniCurses if you want to use UniCurses on a "+sys.platform+" platform.\n")
            raise ImportError("UniCurses initialization error = " + pdcurses + " not found: " + path_to_pdcurses)
        pdlib = ctypes.CDLL(path_to_pdcurses)   # we're on winXX, use pdcurses instead of native ncurses

# +++ PDCurses/NCurses curses.h marco wrappers and other prereqs +++

# A PDC structure for the mouse events
if not NCURSES:
    class MEVENT(ctypes.Structure):
        _fields_ = [("id", ctypes.c_short),
                    ("x", ctypes.c_int),
                    ("y", ctypes.c_int),
                    ("z", ctypes.c_int),
                    ("mmask_t", ctypes.c_ulong)]

# Reconfigure the UniCurses wrapper to use a certain library instead of the default
# PDCurses and the default NCurses. This must be called before initscr().
# Pass an empty string or UCS_DEFAULT_WRAPPER to use the default wrapper.
# !!! THIS IS NOT FOR GENERAL USE AND WILL IN MOST CASES BREAK UNICURSES !!!
# !!! EVEN IF IT DOESN'T MAKE YOUR APP CRASH OR HANG, IT MAY BREAK PORTABILITY !!!
# !!! IF YOU DON'T KNOW WHAT THIS MAY BE USED FOR, YOU DON'T NEED TO USE IT !!!
def ucs_reconfigure(wrapper_ncurses, wrapper_pdcurses):
    global NCURSES
    global NCURSES_AVAILABLE
    global pdlib
    if NCURSES_AVAILABLE:
        if wrapper_ncurses == UCS_DEFAULT_WRAPPER:
            NCURSES = True
        else:
            NCURSES = False
            pdlib = ctypes.CDLL(wrapper_ncurses)
            try:
                pdlib = ctypes.CDLL(wrapper_ncurses)
            except:
                raise Exception("UCS_CONFIGURE: There was an error configuring the NCurses wrapper using the library "+wrapper_ncurses+".")
    else:
        if wrapper_pdcurses == UCS_DEFAULT_WRAPPER:
            NCURSES = False
            try:
                pdlib = ctypes.CDLL("pdcurses.dll")
            except:
                raise Exception("UCS_CONFIGURE: There was an error configuring the default PDCurses wrapper, make sure pdcurses.dll is available in the same folder as UniCurses.")
        else:
            NCURSES = False
            try:
                pdlib = ctypes.CDLL(wrapper_pdcurses)
            except:
                raise Exception("UCS_CONFIGURE: There was an error configuring the PDCurses wrappr using th library "+wrapper_pdcurses+".")


# Return a bytes-encoded C style string from anything that's convertable with str.
# It is used to pass strings to PDCurses which expects a C-formatted string.
def CSTR(s):
    return str(s).encode(code)

# Choose a color pair
def PD_COLOR_PAIR(n):
    return (n << PDC_COLOR_SHIFT) & PDC_A_COLOR

# Pair number from curses.h
def PD_PAIR_NUMBER(n):
    return (n & PDC_A_COLOR) >> PDC_COLOR_SHIFT

# Get the PDC curscr (NOT PORTABLE!)
def PD_GET_CURSCR():
    return ctypes.c_int.in_dll(pdlib, "curscr")

# --- PDCurses/NCurses curses.h macro wrappers and other prereqs ---



# +++ CONSTANTS: PDCurses curses.h +++

if not NCURSES:
    PDC_COLOR_SHIFT = 24
    PDC_ATTR_SHIFT = 19
    PDC_A_NORMAL = 0
    PDC_A_ALTCHARSET = 0x00010000
    PDC_A_BLINK = 0x00400000
    PDC_A_BOLD = 0x00800000
    PDC_A_COLOR = 0xff000000
    PDC_A_DIM = 0
    PDC_A_NORMAL = 0
    PDC_A_REVERSE = 0x00200000
    PDC_A_UNDERLINE = 0x00100000
    PDC_A_STANDOUT = (PDC_A_REVERSE | PDC_A_BOLD)
    PDC_A_RIGHTLINE = 0x00020000
    PDC_A_LEFTLINE = 0x00040000
    PDC_A_INVIS = 0x00080000
    PDC_A_ATTRIBUTES = 0xffff0000
    PDC_A_CHARTEXT = 0x0000ffff
    PDC_A_COLOR = 0xff000000
    PDC_A_ITALIC = PDC_A_INVIS
    PDC_A_PROTECT = (PDC_A_UNDERLINE | PDC_A_LEFTLINE | PDC_A_RIGHTLINE)

# Key mapping (PDC)
if not NCURSES:
    PDC_KEY_CODE_YES =  0x100  # If get_wch() gives a key code 
    PDC_KEY_BREAK    =  0x101  # Not on PC KBD 
    PDC_KEY_DOWN     =  0x102  # Down arrow key 
    PDC_KEY_UP       =  0x103  # Up arrow key 
    PDC_KEY_LEFT     =  0x104  # Left arrow key 
    PDC_KEY_RIGHT    =  0x105  # Right arrow key 
    PDC_KEY_HOME     =  0x106  # home key 
    PDC_KEY_BACKSPACE=  0x107  # not on pc 
    PDC_KEY_F0       =  0x108  # function keys; 64 reserved 
    PDC_KEY_DL       =  0x148  # delete line 
    PDC_KEY_IL       =  0x149  # insert line 
    PDC_KEY_DC       =  0x14a  # delete character 
    PDC_KEY_IC       =  0x14b  # insert char or enter ins mode 
    PDC_KEY_EIC      =  0x14c  # exit insert char mode 
    PDC_KEY_CLEAR    =  0x14d  # clear screen 
    PDC_KEY_EOS      =  0x14e  # clear to end of screen 
    PDC_KEY_EOL      =  0x14f  # clear to end of line 
    PDC_KEY_SF       =  0x150  # scroll 1 line forward 
    PDC_KEY_SR       =  0x151  # scroll 1 line back (reverse) 
    PDC_KEY_NPAGE    =  0x152  # next page 
    PDC_KEY_PPAGE    =  0x153  # previous page 
    PDC_KEY_STAB     =  0x154  # set tab 
    PDC_KEY_CTAB     =  0x155  # clear tab 
    PDC_KEY_CATAB    =  0x156  # clear all tabs 
    PDC_KEY_ENTER    =  0x157  # enter or send (unreliable) 
    PDC_KEY_SRESET   =  0x158  # soft/reset (partial/unreliable) 
    PDC_KEY_RESET    =  0x159  # reset/hard reset (unreliable) 
    PDC_KEY_PRINT    =  0x15a  # print/copy 
    PDC_KEY_LL       =  0x15b  # home down/bottom (lower left) 
    PDC_KEY_ABORT    =  0x15c  # abort/terminate key (any) 
    PDC_KEY_SHELP    =  0x15d  # short help 
    PDC_KEY_LHELP    =  0x15e  # long help 
    PDC_KEY_BTAB     =  0x15f  # Back tab key 
    PDC_KEY_BEG      =  0x160  # beg(inning) key 
    PDC_KEY_CANCEL   =  0x161  # cancel key 
    PDC_KEY_CLOSE    =  0x162  # close key 
    PDC_KEY_COMMAND  =  0x163  # cmd (command) key 
    PDC_KEY_COPY     =  0x164  # copy key 
    PDC_KEY_CREATE   =  0x165  # create key 
    PDC_KEY_END      =  0x166  # end key 
    PDC_KEY_EXIT     =  0x167  # exit key 
    PDC_KEY_FIND     =  0x168  # find key 
    PDC_KEY_HELP     =  0x169  # help key 
    PDC_KEY_MARK     =  0x16a  # mark key 
    PDC_KEY_MESSAGE  =  0x16b  # message key 
    PDC_KEY_MOVE     =  0x16c  # move key 
    PDC_KEY_NEXT     =  0x16d  # next object key 
    PDC_KEY_OPEN     =  0x16e  # open key 
    PDC_KEY_OPTIONS  =  0x16f  # options key 
    PDC_KEY_PREVIOUS =  0x170  # previous object key 
    PDC_KEY_REDO     =  0x171  # redo key 
    PDC_KEY_REFERENCE=  0x172  # ref(erence) key 
    PDC_KEY_REFRESH  =  0x173  # refresh key 
    PDC_KEY_REPLACE  =  0x174  # replace key 
    PDC_KEY_RESTART  =  0x175  # restart key 
    PDC_KEY_RESUME   =  0x176  # resume key 
    PDC_KEY_SAVE     =  0x177  # save key 
    PDC_KEY_SBEG     =  0x178  # shifted beginning key 
    PDC_KEY_SCANCEL  =  0x179  # shifted cancel key 
    PDC_KEY_SCOMMAND =  0x17a  # shifted command key 
    PDC_KEY_SCOPY    =  0x17b  # shifted copy key 
    PDC_KEY_SCREATE  =  0x17c  # shifted create key 
    PDC_KEY_SDC      =  0x17d  # shifted delete char key 
    PDC_KEY_SDL      =  0x17e  # shifted delete line key 
    PDC_KEY_SELECT   =  0x17f  # select key 
    PDC_KEY_SEND     =  0x180  # shifted end key 
    PDC_KEY_SEOL     =  0x181  # shifted clear line key 
    PDC_KEY_SEXIT    =  0x182  # shifted exit key 
    PDC_KEY_SFIND    =  0x183  # shifted find key 
    PDC_KEY_SHOME    =  0x184  # shifted home key 
    PDC_KEY_SIC      =  0x185  # shifted input key 
    PDC_KEY_SLEFT    =  0x187  # shifted left arrow key 
    PDC_KEY_SMESSAGE =  0x188  # shifted message key 
    PDC_KEY_SMOVE    =  0x189  # shifted move key 
    PDC_KEY_SNEXT    =  0x18a  # shifted next key 
    PDC_KEY_SOPTIONS =  0x18b  # shifted options key 
    PDC_KEY_SPREVIOUS=  0x18c  # shifted prev key 
    PDC_KEY_SPRINT   =  0x18d  # shifted print key 
    PDC_KEY_SREDO    =  0x18e  # shifted redo key 
    PDC_KEY_SREPLACE =  0x18f  # shifted replace key 
    PDC_KEY_SRIGHT   =  0x190  # shifted right arrow 
    PDC_KEY_SRSUME   =  0x191  # shifted resume key 
    PDC_KEY_SSAVE    =  0x192  # shifted save key 
    PDC_KEY_SSUSPEND =  0x193  # shifted suspend key 
    PDC_KEY_SUNDO    =  0x194  # shifted undo key 
    PDC_KEY_SUSPEND  =  0x195  # suspend key 
    PDC_KEY_UNDO     =  0x196  # undo key 
    PDC_KEY_A1       =  0x1c1
    PDC_KEY_A3       =  0x1c3
    PDC_KEY_B2       =  0x1c5
    PDC_KEY_C1       =  0x1c7
    PDC_KEY_C3       =  0x1c9
    PDC_KEY_MOUSE    =  0x21b
    PDC_KEY_RESIZE   =  0x222

# Mouse mapping (PDC)
if not NCURSES:
    PDC_BUTTON1_RELEASED       =  0x00000001
    PDC_BUTTON1_PRESSED        =  0x00000002
    PDC_BUTTON1_CLICKED        =  0x00000004
    PDC_BUTTON1_DOUBLE_CLICKED =  0x00000008
    PDC_BUTTON1_TRIPLE_CLICKED =  0x00000010

    PDC_BUTTON2_RELEASED       =  0x00000020
    PDC_BUTTON2_PRESSED        =  0x00000040
    PDC_BUTTON2_CLICKED        =  0x00000080
    PDC_BUTTON2_DOUBLE_CLICKED =  0x00000100
    PDC_BUTTON2_TRIPLE_CLICKED =  0x00000200

    PDC_BUTTON3_RELEASED       =  0x00000400
    PDC_BUTTON3_PRESSED        =  0x00000800
    PDC_BUTTON3_CLICKED        =  0x00001000
    PDC_BUTTON3_DOUBLE_CLICKED =  0x00002000
    PDC_BUTTON3_TRIPLE_CLICKED =  0x00004000

    PDC_BUTTON4_RELEASED       =  0x00008000
    PDC_BUTTON4_PRESSED        =  0x00010000
    PDC_BUTTON4_CLICKED        =  0x00020000
    PDC_BUTTON4_DOUBLE_CLICKED =  0x00040000
    PDC_BUTTON4_TRIPLE_CLICKED =  0x00080000

    PDC_BUTTON_SHIFT           =  0x04000000
    PDC_BUTTON_CTRL            =  0x08000000
    PDC_BUTTON_ALT             =  0x10000000

    PDC_ALL_MOUSE_EVENTS       =  0x1fffffff
    PDC_REPORT_MOUSE_POSITION  =  0x20000000


# +++ CONSTANTS: Platform-independent +++

# General
OK = 0
ERR = -1

# Attributes
if NCURSES:
    A_ALTCHARSET = curses.A_ALTCHARSET
    A_BLINK = curses.A_BLINK
    A_BOLD = curses.A_BOLD
    A_DIM = curses.A_DIM
    A_NORMAL = curses.A_NORMAL
    A_STANDOUT = curses.A_STANDOUT
    A_UNDERLINE = curses.A_UNDERLINE
    A_REVERSE = curses.A_REVERSE
    A_PROTECT = curses.A_PROTECT
    A_ATTRIBUTES = curses.A_ATTRIBUTES
    A_COLOR = curses.A_COLOR
    A_CHARTEXT = curses.A_CHARTEXT
    try:
        A_INVIS = curses.A_INVIS
    except:
        A_INVIS = A_NORMAL
else:
    A_ALTCHARSET = PDC_A_ALTCHARSET
    A_BLINK = PDC_A_BLINK
    A_BOLD = PDC_A_BOLD
    A_DIM = PDC_A_DIM
    A_NORMAL = PDC_A_NORMAL
    A_STANDOUT = PDC_A_STANDOUT
    A_UNDERLINE = PDC_A_UNDERLINE
    A_REVERSE = PDC_A_REVERSE
    A_PROTECT = PDC_A_PROTECT
    A_ATTRIBUTES = PDC_A_ATTRIBUTES
    A_INVIS = PDC_A_INVIS
    A_COLOR = PDC_A_COLOR
    A_CHARTEXT = PDC_A_CHARTEXT

# Colors
if NCURSES:
    COLOR_BLACK=curses.COLOR_BLACK
    COLOR_BLUE=curses.COLOR_BLUE
    COLOR_CYAN=curses.COLOR_CYAN
    COLOR_GREEN=curses.COLOR_GREEN
    COLOR_MAGENTA=curses.COLOR_MAGENTA
    COLOR_RED=curses.COLOR_RED
    COLOR_WHITE=curses.COLOR_WHITE
    COLOR_YELLOW=curses.COLOR_YELLOW
else:
    COLOR_BLACK = 0
    COLOR_BLUE = 1
    COLOR_GREEN = 2
    COLOR_RED = 4
    COLOR_CYAN = (COLOR_BLUE | COLOR_GREEN)
    COLOR_MAGENTA = (COLOR_RED | COLOR_BLUE)
    COLOR_YELLOW = (COLOR_RED | COLOR_GREEN)
    COLOR_WHITE = 7


# Get a C character
def CCHAR(ch):
    if type(ch)==str:
        return ord(ch)
    elif type(ch)==int:
        return ch
    else:
        raise Exception("CCHAR: can't parse a non-char/non-int value.")

# Alternate character set
def ALTCHAR(ch):
    if type(ch)==str:
        return ord(ch) | A_ALTCHARSET
    elif type(ch)==int:
        return ch | A_ALTCHARSET
    else:
        raise Exception("ALTCHAR: can't parse a non-char/non-int value.")


# ACS Alternate Character Set Symbols
ACS_ULCORNER = ALTCHAR('l')
ACS_LLCORNER = ALTCHAR('m')
ACS_URCORNER = ALTCHAR('k')
ACS_LRCORNER = ALTCHAR('j')
ACS_LTEE = ALTCHAR('t')
ACS_RTEE = ALTCHAR('u')
ACS_BTEE = ALTCHAR('v')
ACS_TTEE = ALTCHAR('w')
ACS_HLINE = ALTCHAR('q')
ACS_VLINE = ALTCHAR('x')
ACS_PLUS = ALTCHAR('n')
ACS_S1 = ALTCHAR('o')
ACS_S9 = ALTCHAR('s')
ACS_DIAMOND = ALTCHAR('`')
ACS_CKBOARD = ALTCHAR('a')
ACS_DEGREE = ALTCHAR('f')
ACS_PLMINUS = ALTCHAR('g')
ACS_BULLET = ALTCHAR('~')
ACS_LARROW = ALTCHAR(',')
ACS_RARROW = ALTCHAR('+')
ACS_DARROW = ALTCHAR('.')
ACS_UARROW = ALTCHAR('-')
ACS_BOARD = ALTCHAR('h')
ACS_LANTERN = ALTCHAR('i')
ACS_BLOCK = ALTCHAR('0')
ACS_S3 = ALTCHAR('p')
ACS_S7 = ALTCHAR('r')
ACS_LEQUAL = ALTCHAR('y')
ACS_GEQUAL = ALTCHAR('z')
ACS_PI = ALTCHAR('{')
ACS_NEQUAL = ALTCHAR('|')
ACS_STERLING = ALTCHAR('}')
ACS_BSSB = ACS_ULCORNER
ACS_SSBB = ACS_LLCORNER
ACS_BBSS = ACS_URCORNER
ACS_SBBS = ACS_LRCORNER
ACS_SBSS = ACS_RTEE
ACS_SSSB = ACS_LTEE
ACS_SSBS = ACS_BTEE
ACS_BSSS = ACS_TTEE
ACS_BSBS = ACS_HLINE
ACS_SBSB = ACS_VLINE
ACS_SSSS = ACS_PLUS

# Unicurses-specific: pseudographic mode
SCS_ULCORNER = CCHAR('+')
SCS_LLCORNER = CCHAR('+')
SCS_URCORNER = CCHAR('+')
SCS_LRCORNER = CCHAR('+')
SCS_LTEE = CCHAR('+')
SCS_RTEE = CCHAR('+')
SCS_BTEE = CCHAR('+')
SCS_TTEE = CCHAR('+')
SCS_HLINE = CCHAR('-')
SCS_VLINE = CCHAR('|')
SCS_PLUS = CCHAR('+')
SCS_S1 = CCHAR('-')
SCS_S9 = CCHAR('_')
SCS_DIAMOND = CCHAR('+')
SCS_CKBOARD = CCHAR(':')
SCS_DEGREE = CCHAR('\\')
SCS_PLMINUS = CCHAR('#')
SCS_BULLET = CCHAR('o')
SCS_LARROW = CCHAR('<')
SCS_RARROW = CCHAR('>')
SCS_DARROW = CCHAR('v')
SCS_UARROW = CCHAR('^')
SCS_BOARD = CCHAR('#')
SCS_LANTERN = CCHAR('*')
SCS_BLOCK = CCHAR('#')
SCS_S3 = CCHAR('-')
SCS_S7 = CCHAR('-')
SCS_LEQUAL = CCHAR('<')
SCS_GEQUAL = CCHAR('>')
SCS_PI = CCHAR('n')
SCS_NEQUAL = CCHAR('+')
SCS_STERLING = CCHAR('L')
SCS_BSSB = ACS_ULCORNER
SCS_SSBB = ACS_LLCORNER
SCS_BBSS = ACS_URCORNER
SCS_SBBS = ACS_LRCORNER
SCS_SBSS = ACS_RTEE
SCS_SSSB = ACS_LTEE
SCS_SSBS = ACS_BTEE
SCS_BSSS = ACS_TTEE
SCS_BSBS = ACS_HLINE
SCS_SBSB = ACS_VLINE
SCS_SSSS = ACS_PLUS

# Keymap
if NCURSES:
#   KEY_CODE_YES = curses.KEY_CODE_YES
    KEY_MIN      = curses.KEY_MIN
    KEY_BREAK    = curses.KEY_BREAK
    KEY_SRESET   = curses.KEY_SRESET
    KEY_RESET    = curses.KEY_RESET
    KEY_DOWN     = curses.KEY_DOWN
    KEY_UP       = curses.KEY_UP
    KEY_LEFT     = curses.KEY_LEFT
    KEY_RIGHT    = curses.KEY_RIGHT
    KEY_HOME     = curses.KEY_HOME
    KEY_BACKSPACE= curses.KEY_BACKSPACE
    KEY_F0       = curses.KEY_F0
    KEY_DL       = curses.KEY_DL
    KEY_IL       = curses.KEY_IL
    KEY_DC       = curses.KEY_DC
    KEY_IC       = curses.KEY_IC
    KEY_EIC      = curses.KEY_EIC
    KEY_CLEAR    = curses.KEY_CLEAR
    KEY_EOS      = curses.KEY_EOS
    KEY_EOL      = curses.KEY_EOL
    KEY_SF       = curses.KEY_SF
    KEY_SR       = curses.KEY_SR
    KEY_NPAGE    = curses.KEY_NPAGE
    KEY_PPAGE    = curses.KEY_PPAGE
    KEY_STAB     = curses.KEY_STAB
    KEY_CTAB     = curses.KEY_CTAB
    KEY_CATAB    = curses.KEY_CATAB
    KEY_ENTER    = curses.KEY_ENTER
    KEY_PRINT    = curses.KEY_PRINT
    KEY_LL       = curses.KEY_LL
    KEY_A1       = curses.KEY_A1
    KEY_A3       = curses.KEY_A3
    KEY_B2       = curses.KEY_B2
    KEY_C1       = curses.KEY_C1
    KEY_C3       = curses.KEY_C3
    KEY_BTAB     = curses.KEY_BTAB
    KEY_BEG      = curses.KEY_BEG
    KEY_CANCEL   = curses.KEY_CANCEL
    KEY_CLOSE    = curses.KEY_CLOSE
    KEY_COMMAND  = curses.KEY_COMMAND
    KEY_COPY     = curses.KEY_COPY
    KEY_CREATE   = curses.KEY_CREATE
    KEY_END      = curses.KEY_END
    KEY_EXIT     = curses.KEY_EXIT
    KEY_FIND     = curses.KEY_FIND
    KEY_HELP     = curses.KEY_HELP
    KEY_MARK     = curses.KEY_MARK
    KEY_MESSAGE  = curses.KEY_MESSAGE
    KEY_MOVE     = curses.KEY_MOVE
    KEY_NEXT     = curses.KEY_NEXT
    KEY_OPEN     = curses.KEY_OPEN
    KEY_OPTIONS  = curses.KEY_OPTIONS
    KEY_PREVIOUS = curses.KEY_PREVIOUS
    KEY_REDO     = curses.KEY_REDO
    KEY_REFERENCE= curses.KEY_REFERENCE
    KEY_REFRESH  = curses.KEY_REFRESH
    KEY_REPLACE  = curses.KEY_REPLACE
    KEY_RESTART  = curses.KEY_RESTART
    KEY_RESUME   = curses.KEY_RESUME
    KEY_SAVE     = curses.KEY_SAVE
    KEY_SBEG     = curses.KEY_SBEG
    KEY_SCANCEL  = curses.KEY_SCANCEL
    KEY_SCOMMAND = curses.KEY_SCOMMAND
    KEY_SCOPY    = curses.KEY_SCOPY
    KEY_SCREATE  = curses.KEY_SCREATE
    KEY_SDC      = curses.KEY_SDC
    KEY_SDL      = curses.KEY_SDL
    KEY_SELECT   = curses.KEY_SELECT
    KEY_SEND     = curses.KEY_SEND
    KEY_SEOL     = curses.KEY_SEOL
    KEY_SEXIT    = curses.KEY_SEXIT
    KEY_SFIND    = curses.KEY_SFIND
    KEY_SHELP    = curses.KEY_SHELP
    KEY_SHOME    = curses.KEY_SHOME
    KEY_SIC      = curses.KEY_SIC
    KEY_SLEFT    = curses.KEY_SLEFT
    KEY_SMESSAGE = curses.KEY_SMESSAGE
    KEY_SMOVE    = curses.KEY_SMOVE
    KEY_SNEXT    = curses.KEY_SNEXT
    KEY_SOPTIONS = curses.KEY_SOPTIONS
    KEY_SPREVIOUS= curses.KEY_SPREVIOUS
    KEY_SPRINT   = curses.KEY_SPRINT
    KEY_SREDO    = curses.KEY_SREDO
    KEY_SREPLACE = curses.KEY_SREPLACE
    KEY_SRIGHT   = curses.KEY_SRIGHT
    KEY_SRSUME   = curses.KEY_SRSUME
    KEY_SSAVE    = curses.KEY_SSAVE
    KEY_SSUSPEND = curses.KEY_SSUSPEND
    KEY_SUNDO    = curses.KEY_SUNDO
    KEY_SUSPEND  = curses.KEY_SUSPEND
    KEY_UNDO     = curses.KEY_UNDO
    KEY_MOUSE    = curses.KEY_MOUSE
    KEY_RESIZE   = curses.KEY_RESIZE
#   KEY_EVENT    = curses.KEY_EVENT
    KEY_MAX      = curses.KEY_MAX

else:
#   KEY_CODE_YES = PDC_KEY_CODE_YES
    KEY_MIN      = PDC_KEY_BREAK
    KEY_BREAK    = PDC_KEY_BREAK
    KEY_SRESET   = PDC_KEY_SRESET
    KEY_RESET    = PDC_KEY_RESET
    KEY_DOWN     = PDC_KEY_DOWN
    KEY_UP       = PDC_KEY_UP
    KEY_LEFT     = PDC_KEY_LEFT
    KEY_RIGHT    = PDC_KEY_RIGHT
    KEY_HOME     = PDC_KEY_HOME
    KEY_BACKSPACE= PDC_KEY_BACKSPACE
    KEY_F0       = PDC_KEY_F0
    KEY_DL       = PDC_KEY_DL
    KEY_IL       = PDC_KEY_IL
    KEY_DC       = PDC_KEY_DC
    KEY_IC       = PDC_KEY_IC
    KEY_EIC      = PDC_KEY_EIC
    KEY_CLEAR    = PDC_KEY_CLEAR
    KEY_EOS      = PDC_KEY_EOS
    KEY_EOL      = PDC_KEY_EOL
    KEY_SF       = PDC_KEY_SF
    KEY_SR       = PDC_KEY_SR
    KEY_NPAGE    = PDC_KEY_NPAGE
    KEY_PPAGE    = PDC_KEY_PPAGE
    KEY_STAB     = PDC_KEY_STAB
    KEY_CTAB     = PDC_KEY_CTAB
    KEY_CATAB    = PDC_KEY_CATAB
    KEY_ENTER    = PDC_KEY_ENTER
    KEY_PRINT    = PDC_KEY_PRINT
    KEY_LL       = PDC_KEY_LL
    KEY_A1       = PDC_KEY_A1
    KEY_A3       = PDC_KEY_A3
    KEY_B2       = PDC_KEY_B2
    KEY_C1       = PDC_KEY_C1
    KEY_C3       = PDC_KEY_C3
    KEY_BTAB     = PDC_KEY_BTAB
    KEY_BEG      = PDC_KEY_BEG
    KEY_CANCEL   = PDC_KEY_CANCEL
    KEY_CLOSE    = PDC_KEY_CLOSE
    KEY_COMMAND  = PDC_KEY_COMMAND
    KEY_COPY     = PDC_KEY_COPY
    KEY_CREATE   = PDC_KEY_CREATE
    KEY_END      = PDC_KEY_END
    KEY_EXIT     = PDC_KEY_EXIT
    KEY_FIND     = PDC_KEY_FIND
    KEY_HELP     = PDC_KEY_HELP
    KEY_MARK     = PDC_KEY_MARK
    KEY_MESSAGE  = PDC_KEY_MESSAGE
    KEY_MOVE     = PDC_KEY_MOVE
    KEY_NEXT     = PDC_KEY_NEXT
    KEY_OPEN     = PDC_KEY_OPEN
    KEY_OPTIONS  = PDC_KEY_OPTIONS
    KEY_PREVIOUS = PDC_KEY_PREVIOUS
    KEY_REDO     = PDC_KEY_REDO
    KEY_REFERENCE= PDC_KEY_REFERENCE
    KEY_REFRESH  = PDC_KEY_REFRESH
    KEY_REPLACE  = PDC_KEY_REPLACE
    KEY_RESTART  = PDC_KEY_RESTART
    KEY_RESUME   = PDC_KEY_RESUME
    KEY_SAVE     = PDC_KEY_SAVE
    KEY_SBEG     = PDC_KEY_SBEG
    KEY_SCANCEL  = PDC_KEY_SCANCEL
    KEY_SCOMMAND = PDC_KEY_SCOMMAND
    KEY_SCOPY    = PDC_KEY_SCOPY
    KEY_SCREATE  = PDC_KEY_SCREATE
    KEY_SDC      = PDC_KEY_SDC
    KEY_SDL      = PDC_KEY_SDL
    KEY_SELECT   = PDC_KEY_SELECT
    KEY_SEND     = PDC_KEY_SEND
    KEY_SEOL     = PDC_KEY_SEOL
    KEY_SEXIT    = PDC_KEY_SEXIT
    KEY_SFIND    = PDC_KEY_SFIND
    KEY_SHELP    = PDC_KEY_SHELP
    KEY_SHOME    = PDC_KEY_SHOME
    KEY_SIC      = PDC_KEY_SIC
    KEY_SLEFT    = PDC_KEY_SLEFT
    KEY_SMESSAGE = PDC_KEY_SMESSAGE
    KEY_SMOVE    = PDC_KEY_SMOVE
    KEY_SNEXT    = PDC_KEY_SNEXT
    KEY_SOPTIONS = PDC_KEY_SOPTIONS
    KEY_SPREVIOUS= PDC_KEY_SPREVIOUS
    KEY_SPRINT   = PDC_KEY_SPRINT
    KEY_SREDO    = PDC_KEY_SREDO
    KEY_SREPLACE = PDC_KEY_SREPLACE
    KEY_SRIGHT   = PDC_KEY_SRIGHT
    KEY_SRSUME   = PDC_KEY_SRSUME
    KEY_SSAVE    = PDC_KEY_SSAVE
    KEY_SSUSPEND = PDC_KEY_SSUSPEND
    KEY_SUNDO    = PDC_KEY_SUNDO
    KEY_SUSPEND  = PDC_KEY_SUSPEND
    KEY_UNDO     = PDC_KEY_UNDO
    KEY_MOUSE    = PDC_KEY_MOUSE
    KEY_RESIZE   = PDC_KEY_RESIZE
#   KEY_EVENT    = PDC_KEY_EVENT
    KEY_MAX      = 0x224 # == KEY_SDOWN, take that into account

def KEY_F(n): return KEY_F0 + n    # function keys 1-64

# Mouse mapping
if NCURSES:
    BUTTON1_RELEASED = curses.BUTTON1_RELEASED      
    BUTTON1_PRESSED = curses.BUTTON1_PRESSED
    BUTTON1_CLICKED = curses.BUTTON1_CLICKED       
    BUTTON1_DOUBLE_CLICKED = curses.BUTTON1_DOUBLE_CLICKED
    BUTTON1_TRIPLE_CLICKED = curses.BUTTON1_TRIPLE_CLICKED
                          
    BUTTON2_RELEASED = curses.BUTTON2_RELEASED     
    BUTTON2_PRESSED = curses.BUTTON2_PRESSED       
    BUTTON2_CLICKED = curses.BUTTON2_CLICKED       
    BUTTON2_DOUBLE_CLICKED = curses.BUTTON2_DOUBLE_CLICKED
    BUTTON2_TRIPLE_CLICKED = curses.BUTTON2_TRIPLE_CLICKED
                          
    BUTTON3_RELEASED = curses.BUTTON3_RELEASED      
    BUTTON3_PRESSED = curses.BUTTON3_PRESSED
    BUTTON3_CLICKED = curses.BUTTON3_CLICKED       
    BUTTON3_DOUBLE_CLICKED = curses.BUTTON3_DOUBLE_CLICKED
    BUTTON3_TRIPLE_CLICKED = curses.BUTTON3_TRIPLE_CLICKED
                          
    BUTTON4_RELEASED = curses.BUTTON4_RELEASED      
    BUTTON4_PRESSED = curses.BUTTON4_PRESSED       
    BUTTON4_CLICKED = curses.BUTTON4_CLICKED       
    BUTTON4_DOUBLE_CLICKED = curses.BUTTON4_DOUBLE_CLICKED
    BUTTON4_TRIPLE_CLICKED = curses.BUTTON4_TRIPLE_CLICKED
                          
    BUTTON_SHIFT = curses.BUTTON_SHIFT          
    BUTTON_CTRL = curses.BUTTON_CTRL           
    BUTTON_ALT = curses.BUTTON_ALT            
                          
    ALL_MOUSE_EVENTS = curses.ALL_MOUSE_EVENTS      
    REPORT_MOUSE_POSITION = curses.REPORT_MOUSE_POSITION 
else:
    BUTTON1_RELEASED = PDC_BUTTON1_RELEASED      
    BUTTON1_PRESSED = PDC_BUTTON1_PRESSED
    BUTTON1_CLICKED = PDC_BUTTON1_CLICKED       
    BUTTON1_DOUBLE_CLICKED = PDC_BUTTON1_DOUBLE_CLICKED
    BUTTON1_TRIPLE_CLICKED = PDC_BUTTON1_TRIPLE_CLICKED
                          
    BUTTON2_RELEASED = PDC_BUTTON2_RELEASED     
    BUTTON2_PRESSED = PDC_BUTTON2_PRESSED       
    BUTTON2_CLICKED = PDC_BUTTON2_CLICKED       
    BUTTON2_DOUBLE_CLICKED = PDC_BUTTON2_DOUBLE_CLICKED
    BUTTON2_TRIPLE_CLICKED = PDC_BUTTON2_TRIPLE_CLICKED
                          
    BUTTON3_RELEASED = PDC_BUTTON3_RELEASED      
    BUTTON3_PRESSED = PDC_BUTTON3_PRESSED
    BUTTON3_CLICKED = PDC_BUTTON3_CLICKED       
    BUTTON3_DOUBLE_CLICKED = PDC_BUTTON3_DOUBLE_CLICKED
    BUTTON3_TRIPLE_CLICKED = PDC_BUTTON3_TRIPLE_CLICKED
                          
    BUTTON4_RELEASED = PDC_BUTTON4_RELEASED      
    BUTTON4_PRESSED = PDC_BUTTON4_PRESSED       
    BUTTON4_CLICKED = PDC_BUTTON4_CLICKED       
    BUTTON4_DOUBLE_CLICKED = PDC_BUTTON4_DOUBLE_CLICKED
    BUTTON4_TRIPLE_CLICKED = PDC_BUTTON4_TRIPLE_CLICKED
                          
    BUTTON_SHIFT = PDC_BUTTON_SHIFT          
    BUTTON_CTRL = PDC_BUTTON_CTRL           
    BUTTON_ALT = PDC_BUTTON_ALT            
         
    ALL_MOUSE_EVENTS = PDC_ALL_MOUSE_EVENTS      
    REPORT_MOUSE_POSITION = PDC_REPORT_MOUSE_POSITION 

# --- CONSTANTS ---




# +++ FUNCTION DEFINITIONS (PDC) +++

if not NCURSES:
    pdlib.erasechar.restype = ctypes.c_char
    pdlib.keyname.restype = ctypes.c_char_p
    pdlib.killchar.restype = ctypes.c_char
    pdlib.longname.restype = ctypes.c_char_p
    pdlib.nc_getmouse.restype = MEVENT
    pdlib.termattrs.restype = ctypes.c_ulong
    pdlib.termname.restype = ctypes.c_char_p
    pdlib.winch.restype = ctypes.c_uint
    pdlib.mvwinch.restype = ctypes.c_uint
    pdlib.unctrl.restype = ctypes.c_char_p
    pdlib.is_wintouched.restype = ctypes.c_bool
    pdlib.is_linetouched.restype = ctypes.c_bool
    pdlib.can_change_color.restype = ctypes.c_bool
    pdlib.has_colors.restype = ctypes.c_bool
    pdlib.has_ic.restype = ctypes.c_bool
    pdlib.has_il.restype = ctypes.c_bool
    pdlib.has_key.restype = ctypes.c_bool
    pdlib.isendwin.restype = ctypes.c_bool

# --- FUNCTION DEFINITIONS (PDC) ---




# +++ UNIFIED CURSES +++


# functions
def waddch(scr_id, ch, attr=A_NORMAL):
    if NCURSES:
        try:
            return scr_id.addch(ch, attr)
        except curses.error:
            return ERR
    else:
        return pdlib.waddch(scr_id, ch | attr)

def waddstr(scr_id, cstr, attr="NO_USE"):
    if NCURSES:
        try:
            if (attr != "NO_USE"): return scr_id.addstr(str(cstr), attr)
            return scr_id.addstr(str(cstr))
        except curses.error:
            return ERR
    else:
        if (attr != "NO_USE"): oldattr = pdlib.getattrs(scr_id); pdlib.wattrset(scr_id, attr)
        ret = pdlib.waddstr(scr_id, CSTR(cstr))
        if (attr != "NO_USE"): pdlib.wattrset(scr_id, oldattr)
        return ret

def waddnstr(scr_id, cstr, n, attr="NO_USE"):
    if NCURSES:
        try:
            if (attr != "NO_USE"): return scr_id.addnstr(str(cstr), n, int(attr))
            return scr_id.addnstr(str(cstr), n)
        except curses.error:
            return ERR
    else:
        if (attr != "NO_USE"): oldattr = pdlib.getattrs(scr_id); pdlib.wattrset(scr_id, attr)
        ret = pdlib.waddnstr(scr_id, CSTR(cstr), n)
        if (attr != "NO_USE"): pdlib.wattrset(scr_id, oldattr)
        return ret

def wattroff(scr_id, attr):
    if NCURSES:
        try:
            return scr_id.attroff(attr)
        except curses.error:
            return ERR
    else:
        return pdlib.wattroff(scr_id, attr)

def wattron(scr_id, attr):
    if NCURSES:
        try:
            return scr_id.attron(attr)
        except curses.error:
            return ERR
    else:
        return pdlib.wattron(scr_id, attr)

def wattrset(scr_id, attr):
    if NCURSES:
        try:
            return scr_id.attrset(attr)
        except curses.error:
            return ERR
    else:
        return pdlib.wattrset(scr_id, attr)

def baudrate():
    if NCURSES:
        try:
            return curses.baudrate()
        except curses.error:
            return ERR
    else:
        return pdlib.baudrate()

def beep():
    if NCURSES:
        try:
            return curses.beep()
        except curses.error:
            return ERR
    else:
        return pdlib.beep()

def wbkgd(scr_id, ch, attr=A_NORMAL):
    if NCURSES:
        try:
            return scr_id.bkgd(ch, attr)
        except curses.error:
            return ERR
    else:
        return pdlib.wbkgd(scr_id, ch | attr)

def wbkgdset(scr_id, ch, attr=A_NORMAL):
    if NCURSES:
        try:
            return scr_id.bkgdset(ch, attr)
        except curses.error:
            return ERR
    else:
        return pdlib.wbkgdset(scr_id, ch | attr)

def wborder(scr_id, ls=ACS_VLINE, rs=ACS_VLINE, ts=ACS_HLINE, bs=ACS_HLINE, tl=ACS_ULCORNER, tr=ACS_URCORNER, bl=ACS_LLCORNER, br=ACS_LRCORNER):
    if NCURSES:
        try:
            return scr_id.border(ls, rs, ts, bs, tl, tr, bl, br)
        except curses.error:
            return ERR
    else:
        return pdlib.wborder(scr_id, ls, rs, ts, bs, tl, tr, bl, br)

def box(scr_id, verch=ACS_VLINE, horch=ACS_HLINE):
    if NCURSES:
        try:
            return scr_id.box(verch, horch)
        except curses.error:
            return ERR
    else:
        return pdlib.box(scr_id, verch, horch)

def can_change_color():
    if NCURSES:
        try:
            return curses.can_change_color()
        except curses.error:
            return ERR
    else:
        return (pdlib.can_change_color() == 1)

def cbreak():
    if NCURSES:
        try:
            return curses.cbreak()
        except curses.error:
            return ERR
    else:
        return pdlib.cbreak()

def wchgat(scr_id, num, attr, color, opts=None):
    if NCURSES:
        try:
            return scr_id.chgat(num, attr | color_pair(color))
        except curses.error:
            return ERR
    else:
        return pdlib.wchgat(scr_id, num, attr, color, None)

def color_content(color_number):
    if NCURSES:
        try:
            return curses.color_content(color_number)
        except curses.error:
            return ERR
    else:
        r = ctypes.c_short()
        g = ctypes.c_short()
        b = ctypes.c_short()
        pdlib.color_content(color_number, ctypes.byref(r), ctypes.byref(g), ctypes.byref(b))
        return (r.value, g.value, b.value)

def color_pair(color_number):
    if NCURSES:
        try:
            return curses.color_pair(color_number)
        except curses.error:
            return ERR
    else:
        return PD_COLOR_PAIR(color_number)   

def COLOR_PAIR(n): return color_pair(n)

def copywin(src_id, dest_id, sminrow, smincol, dminrow, dmincol, dmaxrow, dmaxcol, overlay):
    if NCURSES:
        try:
            if overlay:
                return src_id.overlay(dest_id, sminrow, smincol, dminrow, dmincol, dmaxrow, dmaxcol)
            else:
                return src_id.overwrite(dest_id, sminrow, smincol, dminrow, dmincol, dmaxrow, dmaxcol)
        except curses.error:
            return ERR
    else:
        return pdlib.copywin(src_id, dest_id, sminrow, smincol, dminrow, dmincol, dmaxrow, dmaxcol, overlay)
    
def wclear(scr_id):
    if NCURSES:
        try:
            return scr_id.clear()
        except curses.error:
            return ERR
    else:
        return pdlib.wclear(scr_id)

def wclrtobot(scr_id):
    if NCURSES:
        try:
            return scr_id.clrtobot()
        except curses.error:
            return ERR
    else:
        return pdlib.wclrtobot(scr_id)

def wclrtoeol(scr_id):
    if NCURSES:
        try:
            return scr_id.clrtoeol()
        except curses.error:
            return ERR
    else:
        return pdlib.wclrtoeol(scr_id)

def clearok(scr_id, yes):
    if NCURSES:
        try:
            return scr_id.clearok(yes)
        except curses.error:
            return ERR
    else:
        return pdlib.clearok(scr_id, yes)

def curs_set(visibility):
    if NCURSES:
        try:
            return curses.curs_set(visibility)
        except curses.error:
            return ERR
    else:
        return pdlib.curs_set(visibility)

def cursyncup(scr_id):
    if NCURSES:
        try:
            return scr_id.cursyncup()
        except curses.error:
            return ERR
    else:
        return pdlib.wcursyncup(scr_id)

def def_prog_mode():
    if NCURSES:
        try:
            return curses.def_prog_mode()
        except curses.error:
            return ERR
    else:
        return pdlib.def_prog_mode()

def def_shell_mode():
    if NCURSES:
        try:
            return curses.def_shell_mode()
        except curses.error:
            return ERR
    else:
        return pdlib.def_shell_mode()

def delay_output(ms):
    if NCURSES:
        try:
            return curses.delay_output(ms)
        except curses.error:
            return ERR
    else:
        return pdlib.delay_output(ms)

def wdelch(scr_id):
    if NCURSES:
        try:
            return scr_id.delch()
        except curses.error:
            return ERR
    else:
        return pdlib.wdelch(scr_id)

def wdeleteln(scr_id):
    if NCURSES:
        try:
            return scr_id.deleteln()
        except curses.error:
            return ERR
    else:
        return pdlib.wdeleteln(scr_id)

def delwin(scr_id):
    if NCURSES:
        try:
            del(scr_id)
            return OK
        except curses.error:
            return ERR
    else:
        return pdlib.delwin(scr_id)

def derwin(srcwin, nlines, ncols, begin_y, begin_x):
    if NCURSES:
        try:
            return srcwin.derwin(nlines, ncols, begin_y, begin_x)
        except curses.error:
            return ERR
    else:
        pdlib.derwin.restype = ctypes.c_void_p	
        return ctypes.c_void_p(pdlib.derwin(srcwin, nlines, ncols, begin_y, begin_x))

def doupdate():
    if NCURSES:
        try:
            return curses.doupdate()
        except curses.error:
            return ERR
    else:
        return pdlib.doupdate()

def echo():
    if NCURSES:
        try:
            return curses.echo()
        except curses.error:
            return ERR
    else:
        return pdlib.echo()

def wechochar(scr_id, ch, attr=A_NORMAL):
    if NCURSES:
        try:
            return scr_id.echochar(ch | attr)
        except curses.error:
            return ERR
    else:
        return pdlib.wechochar(scr_id, ch | attr)

def wenclose(scr_id, y, x):
    if NCURSES:
        try:
            return scr_id.enclose(y, x)
        except curses.error:
            return ERR
    else:
        return pdlib.wenclose(scr_id, y, x)

def endwin():
    if NCURSES:
        try:
            return curses.endwin()
        except curses.error:
            return ERR
    else:
        return pdlib.endwin()

def werase(scr_id):
    if NCURSES:
        try:
            return scr_id.erase()
        except curses.error:
            return ERR
    else:
        return pdlib.werase(scr_id)

def erasechar():   # TODO: this might not be portable across platforms yet
    if NCURSES:
        try:
            return curses.erasechar()
        except curses.error:
            return ERR
    else:
        return pdlib.erasechar()

def filter():
    if NCURSES:
        try:
            return curses.filter()
        except curses.error:
            return ERR
    else:
        return pdlib.filter()

def flash():
    if NCURSES:
        try:
            return curses.flash()
        except curses.error:
            return ERR
    else:
        return pdlib.flash()

def flushinp():
    if NCURSES:
        try:
            return curses.flushinp()
        except curses.error:
            return ERR
    else:
        return pdlib.flushinp()

def getbegyx(scr_id):
    if NCURSES:
        try:
            return scr_id.getbegyx()
        except curses.error:
            return ERR
    else:
        y = pdlib.getbegy(scr_id)
        x = pdlib.getbegx(scr_id)
        return (y, x)

def wgetch(scr_id):
    if NCURSES:
        try:
            return scr_id.getch()
        except curses.error:
            return ERR
    else:
        return pdlib.wgetch(scr_id)

def wgetkey(scr_id, y=-1, x=-1):
    if NCURSES:
        try:
            if (y == -1) or (x == -1): return scr_id.getkey()
            return scr_id.getkey(y, x)
        except curses.error:
            return ERR
    else:
        if (y == -1) or (x == -1): return pdlib.keyname(wgetch(scr_id))
        return pdlib.keyname(mvwgetch(scr_id, y, x)).decode()


def getmaxyx(scr_id):
    if NCURSES:
        try:
            return scr_id.getmaxyx()
        except curses.error:
            return ERR
    else:
        y = pdlib.getmaxy(scr_id)
        x = pdlib.getmaxx(scr_id)
        return (y, x)

def getmouse():
    if NCURSES:
        try:
            return curses.getmouse()
        except curses.error:
            return ERR
    else:
        m_event = pdlib.nc_getmouse()
        return (m_event.id, m_event.x, m_event.y, m_event.z, m_event.mmask_t)

def getparyx(scr_id):
    if NCURSES:
        try:
            return scr_id.getparyx()
        except curses.error:
            return ERR
    else:
        y = pdlib.getpary(scr_id)
        x = pdlib.getparx(scr_id)
        return (y, x)

def wgetstr(scr_id):
    if NCURSES:
        try:
            return scr_id.getstr()
        except curses.error:
            return ERR
    else:
        t_str = ctypes.create_string_buffer(1023)
        pdlib.wgetstr(scr_id, ctypes.byref(t_str))
        return t_str.value.decode()

def getsyx():
    global PDC_LEAVEOK
    if NCURSES:
        try:
            return curses.getsyx()
        except curses.error:
            return ERR
    else:
        if PDC_LEAVEOK: return (-1, -1)
        curscr = PD_GET_CURSCR()
        return getyx(curscr)

def getwin(file):   # THIS IS NOT CROSS-PLATFORM YET, AVOID IF POSSIBLE
    if NCURSES:
        try:
            return curses.getwin(file)
        except curses.error:
            return ERR
    else:
        raise Exception("UNICURSES_GETWIN: 'getwin' is unavailable under Windows!")

def getyx(scr_id):
    if NCURSES:
        try:
            return scr_id.getyx()
        except curses.error:
            return ERR
    else:
        cy = pdlib.getcury(scr_id)
        cx = pdlib.getcurx(scr_id)
        return (cy,cx)

def halfdelay(tenths):
    if NCURSES:
        try:
            return curses.halfdelay(tenths)
        except curses.error:
            return ERR
    else:
        return pdlib.halfdelay(tenths)

def has_colors():
    if NCURSES:
        try:
            return curses.has_colors()
        except curses.error:
            return ERR
    else:
        return (pdlib.has_colors() == 1)

def has_ic():
    if NCURSES:
        try:
            return curses.has_ic()
        except curses.error:
            return ERR
    else:
        return (pdlib.has_ic() == 1)

def has_il():
    if NCURSES:
        try:
            return curses.has_il()
        except curses.error:
            return ERR
    else:
        return (pdlib.has_il() == 1)

def has_key(ch):
    if NCURSES:
        try:
            return curses.has_key(ch)
        except curses.error:
            return ERR
    else:
        return (pdlib.has_key(ch) == 1)

def whline(scr_id, ch, n):
    if NCURSES:
        try:
            return scr_id.hline(ch, n)
        except curses.error:
            return ERR
    else:
        return pdlib.whline(scr_id, ch, n)

def idcok(scr_id, flag):    # THIS IS NOT PORTABLE (IT'S NOP ON PDCURSES)
    if NCURSES:
        try:
            return scr_id.idcok(flag)
        except curses.error:
            return ERR
    else:
        return pdlib.idcok(scr_id, flag)

def idlok(scr_id, yes):     # THIS IS NOT PORTABLE (IT'S NOP ON PDCURSES)
    if NCURSES:
        try:
            return scr_id.idlok(yes)
        except curses.error:
            return ERR
    else:
        return pdlib.idlok(scr_id, yes)

def immedok(scr_id, flag):
    if NCURSES:
        try:
            return scr_id.immedok(flag)
        except curses.error:
            return ERR
    else:
        return pdlib.immedok(scr_id, flag)

def winch(scr_id):
    if NCURSES:
        try:
            return scr_id.inch()
        except curses.error:
            return ERR
    else:
        return pdlib.winch(scr_id)

def init_color(color, r, g, b):
    if NCURSES:
        try:
            return curses.init_color(color, r, g, b)
        except curses.error:
            return ERR
    else:
        return pdlib.init_color(color, r, g, b)

def init_pair(pair_number, fg, bg):
    if NCURSES:
        try:
            return curses.init_pair(pair_number, fg, bg)
        except curses.error:
            return ERR
    else:
        return pdlib.init_pair(pair_number, fg, bg)

def initscr():
    global stdscr
    if NCURSES:
        try:
            stdscr = curses.initscr()
            return stdscr
        except curses.error:
            return ERR
    else:
        pdlib.initscr.restype = ctypes.c_void_p
        stdscr = ctypes.c_void_p(pdlib.initscr())
        return stdscr

def winsch(scr_id, ch, attr=A_NORMAL):
    if NCURSES:
        try:
            return scr_id.insch(ch, attr)
        except curses.error:
            return ERR
    else:
        return pdlib.winsch(scr_id, ch | attr)

def winsdelln(scr_id, nlines):
    if NCURSES:
        try:
            return scr_id.insdelln(nlines)
        except curses.error:
            return ERR
    else:
        return pdlib.winsdelln(scr_id, nlines)

def winsstr(scr_id, strn, attr = "NO_USE"):
    if NCURSES:
        try:
            if (attr != "NO_USE"): return scr_id.insstr(str(strn), attr)
            return scr_id.insstr(str(strn))
        except curses.error:
            return ERR
    else:
        oldattr = 0
        if (attr != "NO_USE"): oldattr = pdlib.getattrs(scr_id); pdlib.wattrset(scr_id, attr)
        ret = pdlib.winsstr(scr_id, CSTR(strn))
        if (attr != "NO_USE"): pdlib.wattrset(scr_id, oldattr)
        return ret

def winsnstr(scr_id, strn, n, attr = "NO_USE"):
    if NCURSES:
        try:
            if (attr != "NO_USE"): return scr_id.insnstr(str(strn), n, attr)
            return scr_id.insnstr(str(strn), n)
        except curses.error:
            return ERR
    else:
        oldattr = 0
        if (attr != "NO_USE"): oldattr = pdlib.getattrs(scr_id); pdlib.wattrset(scr_id, attr)
        ret = pdlib.winsnstr(scr_id, CSTR(strn), n)
        if (attr != "NO_USE"): pdlib.wattrset(scr_id, oldattr)
        return ret

def winstr(scr_id, n=-1):
    if NCURSES:
        try:
            return scr_id.instr(n)
        except curses.error:
            return ERR
    else:
        t_str = ctypes.create_string_buffer(1023)
        pdlib.winnstr(scr_id, ctypes.byref(t_str), n)
        return t_str.value.decode()

def isendwin():
    if NCURSES:
        try:
            return curses.isendwin()
        except curses.error:
            return ERR
    else:
        return (pdlib.isendwin() == 1)

def winsertln(scr_id):
    if NCURSES:
        try:
            return scr_id.insertln()
        except curses.error:
            return ERR
    else:
        return pdlib.winsertln(scr_id)

def is_linetouched(scr_id, line):
    if NCURSES:
        try:
            return scr_id.is_linetouched(line)
        except curses.error:
            return ERR
    else:
        return (pdlib.is_linetouched(scr_id, line) == 1)

def is_wintouched(scr_id):
    if NCURSES:
        try:
            return scr_id.is_wintouched()
        except curses.error:
            return ERR
    else:
        return (pdlib.is_wintouched(scr_id) == 1)

def keyname(k):
    if NCURSES:
        try:
            return curses.keyname(k)
        except curses.error:
            return ERR
    else:
        return pdlib.keyname(k).decode()

def keypad(scr_id, yes):
    if NCURSES:
        try:
            return scr_id.keypad(yes)
        except curses.error:
            return ERR
    else:
        return pdlib.keypad(scr_id, yes)

def killchar():   # TODO: this might not be portable across platforms yet
    if NCURSES:
        try:
            return curses.killchar()
        except curses.error:
            return ERR
    else:
        return pdlib.killchar()

def leaveok(scr_id, yes):
    global PDC_LEAVEOK
    if NCURSES:
        try:
            return scr_id.leaveok(yes)
        except curses.error:
            return ERR
    else:
        if scr_id.value == PD_GET_CURSCR().value:
            PDC_LEAVEOK = yes
        return pdlib.leaveok(scr_id, yes)

def longname():
    if NCURSES:
        try:
            return curses.longname()
        except curses.error:
            return ERR
    else:
        return pdlib.longname().decode()

def meta(scr_id, yes):
    if NCURSES:
        try:
            return curses.meta(yes)
        except curses.error:
            return ERR
    else:
        return pdlib.meta(scr_id, yes)

def mouseinterval(interval):
    if NCURSES:
        try:
            return curses.mouseinterval(interval)
        except curses.error:
            return ERR
    else:
        return pdlib.mouseinterval(interval)

def mousemask(mmask):
    if NCURSES:
        try:
            return curses.mousemask(mmask)
        except curses.error:
            return ERR
    else:
        return pdlib.mousemask(mmask, None)

def wmove(scr_id, new_y, new_x):
    if NCURSES:
        try:
            return scr_id.move(new_y, new_x)
        except curses.error:
            return ERR
    else:
        return pdlib.wmove(scr_id, new_y, new_x)

def mvwaddch(scr_id, y, x, ch, attr=A_NORMAL):
    if NCURSES:
        try:
            return scr_id.addch(y, x, ch, attr)
        except curses.error:
            return ERR
    else:
        return pdlib.mvwaddch(scr_id, y, x, ch | attr)

def mvwaddstr(scr_id, y, x, cstr, attr="NO_USE"):
    if NCURSES:
        try:
            if (attr != "NO_USE"): return scr_id.addstr(y, x, str(cstr), attr)
            return scr_id.addstr(y, x, str(cstr))
        except curses.error:
            return ERR
    else:
        if (attr != "NO_USE"): oldattr = pdlib.getattrs(scr_id); pdlib.wattrset(scr_id, attr)
        ret = pdlib.mvwaddstr(scr_id, y, x, CSTR(cstr))
        if (attr != "NO_USE"): pdlib.wattrset(scr_id, oldattr)
        return ret

def mvwaddnstr(scr_id, y, x, cstr, n, attr="NO_USE"):
    if NCURSES:
        try:
            if (attr != "NO_USE"): return scr_id.addnstr(y, x, str(cstr), n, attr)
            return scr_id.addnstr(y, x, str(cstr), n)
        except curses.error:
            return ERR
    else:
        if (attr != "NO_USE"): oldattr = pdlib.getattrs(scr_id); pdlib.wattrset(scr_id, attr)
        ret = pdlib.mvwaddnstr(scr_id, y, x, CSTR(cstr), n)
        if (attr != "NO_USE"): pdlib.wattrset(scr_id, oldattr)
        return ret

def mvwchgat(scr_id, y, x, num, attr, color, opts=None):
    if NCURSES:
        try:
            return scr_id.chgat(y, x, num, attr | color_pair(color))
        except curses.error:
            return ERR
    else:
        return pdlib.mvwchgat(scr_id, y, x, num, attr, color, None)

def mvwdelch(scr_id, y, x):
    if NCURSES:
        try:
            return scr_id.delch(y,x)
        except curses.error:
            return ERR
    else:
        return pdlib.mvwdelch(scr_id, y, x)

def mvwdeleteln(scr_id, y, x):
    if NCURSES:
        try:
            move(scr_id, y, x)
            return scr_id.deleteln()
        except curses.error:
            return ERR
    else:
        return pdlib.mvwdeleteln(scr_id, y, x)

def mvderwin(scr_id, pary, parx):
    if NCURSES:
        try:
            return scr_id.mvderwin(pary, parx)
        except curses.error:
            return ERR
    else:
        return pdlib.mvderwin(scr_id, pary, parx)

def mvwgetch(scr_id, y, x):
    if NCURSES:
        try:
            return scr_id.getch(y, x)
        except curses.error:
            return ERR
    else:
        return pdlib.mvwgetch(scr_id, y, x)

def mvwgetstr(scr_id, y, x):
    if NCURSES:
        try:
            return scr_id.getstr(y, x)
        except curses.error:
            return ERR
    else:
        t_str = ctypes.create_string_buffer(1023)
        pdlib.mvwgetstr(scr_id, y, x, ctypes.byref(t_str))
        return t_str.value.decode()

def mvwhline(scr_id, y, x, ch, n):
    if NCURSES:
        try:
            return scr_id.hline(y, x, ch, n)
        except curses.error:
            return ERR
    else:
        return pdlib.mvwhline(scr_id, y, x, ch, n)

def mvwinch(scr_id, y, x):
    if NCURSES:
        try:
            return scr_id.inch(y, x)
        except curses.error:
            return ERR
    else:
        return pdlib.mvwinch(scr_id, y, x)

def mvwinsch(scr_id, y, x, ch, attr=A_NORMAL):
    if NCURSES:
        try:
            return scr_id.insch(y, x, ch, attr)
        except curses.error:
            return ERR
    else:
        return pdlib.mvwinsch(scr_id, y, x, ch | attr)

def mvwinsstr(scr_id, y, x, strn, attr = "NO_USE"):
    if NCURSES:
        try:
            if (attr != "NO_USE"): return scr_id.insstr(y, x, str(strn), attr)
            return scr_id.insstr(y, x, str(strn))
        except curses.error:
            return ERR
    else:
        oldattr = 0
        if (attr != "NO_USE"): oldattr = pdlib.getattrs(scr_id); pdlib.wattrset(scr_id, attr)
        ret = pdlib.mvwinsstr(scr_id, y, x, CSTR(strn))
        if (attr != "NO_USE"): pdlib.wattrset(scr_id, oldattr)
        return ret

def mvwinsnstr(scr_id, y, x, strn, n, attr = "NO_USE"):
    if NCURSES:
        try:
            if (attr != "NO_USE"): return scr_id.insnstr(y, x, str(strn), n, attr)
            return scr_id.insnstr(y, x, str(strn), n)
        except curses.error:
            return ERR
    else:
        oldattr = 0
        if (attr != "NO_USE"): oldattr = pdlib.getattrs(scr_id); pdlib.wattrset(scr_id, attr)
        ret = pdlib.mvwinsnstr(scr_id, y, x, CSTR(strn), n)
        if (attr != "NO_USE"): pdlib.wattrset(scr_id, oldattr)
        return ret

def mvwinstr(scr_id, y, x, n=-1):
    if NCURSES:
        try:
            return scr_id.instr(y, x, n)
        except curses.error:
            return ERR
    else:
        t_str = ctypes.create_string_buffer(1023)
        pdlib.mvwinnstr(scr_id, y, x, ctypes.byref(t_str), n)
        return t_str.value.decode()

def mvwvline(scr_id, y, x, ch, n):
    if NCURSES:
        try:
            return scr_id.vline(y, x, ch, n)
        except curses.error:
            return ERR
    else:
        return pdlib.mvwvline(scr_id, y, x, ch, n)

def mvwin(scr_id, y, x):
    if NCURSES:
        try:
            return scr_id.mvwin(y, x)
        except curses.error:
            return ERR
    else:
        return pdlib.mvwin(scr_id, y, x)

def napms(ms):
    if NCURSES:
        try:
            return curses.napms(ms)
        except curses.error:
            return ERR
    else:
        return pdlib.napms(ms)

def newpad(nlines, ncols):
    if NCURSES:
        try:
            return curses.newpad(nlines, ncols)
        except curses.error:
            return ERR
    else:
        pdlib.newpad.restype = ctypes.c_void_p	
        return ctypes.c_void_p(pdlib.newpad(nlines, ncols))

def newwin(nlines, ncols, begin_y, begin_x):
    if NCURSES:
        try:
            return curses.newwin(nlines, ncols, begin_y, begin_x)
        except curses.error:
            return ERR
    else:
        pdlib.newwin.restype = ctypes.c_void_p
        return ctypes.c_void_p(pdlib.newwin(nlines, ncols, begin_y, begin_x))

def nl(): 
    if NCURSES:
        try:
            return curses.nl()
        except curses.error:
            return ERR
    else:
         return pdlib.nl()

def nocbreak():
    if NCURSES:
        try:
            return curses.nocbreak()
        except curses.error:
            return ERR
    else:
        return pdlib.nocbreak()

def nodelay(scr_id, yes):
    if NCURSES:
        try:
            return scr_id.nodelay(yes)
        except curses.error:
            return ERR
    else:
        return pdlib.nodelay(scr_id, yes)

def noecho():
    if NCURSES:
        try:
            return curses.noecho()
        except curses.error:
            return ERR
    else:
        return pdlib.noecho()

def nonl(): 
    if NCURSES:
        try:
            return curses.nonl()
        except curses.error:
            return ERR
    else:
        return pdlib.nonl()

def noqiflush():
    if NCURSES:
        try:
            return curses.noqiflush()
        except curses.error:
            return ERR
    else:
        return pdlib.noqiflush()

def noraw():
    if NCURSES:
        try:
            return curses.noraw()
        except curses.error:
            return ERR
    else:
        return pdlib.noraw()

def notimeout(scr_id, yes):
    if NCURSES:
        try:
            return scr_id.notimeout(yes)
        except curses.error:
            return ERR
    else:
        return pdlib.notimeout(scr_id, yes)

def noutrefresh(scr_id):
    if NCURSES:
        try:
            return scr_id.noutrefresh()
        except curses.error:
            return ERR
    else:
        return pdlib.wnoutrefresh(scr_id)

def overlay(src_id, dest_id):
    if NCURSES:
        try:
            return src_id.overlay(dest_id)
        except curses.error:
            return ERR
    else:
        return pdlib.overlay(src_id, dest_id)

def overwrite(src_id, dest_id):
    if NCURSES:
        try:
            return src_id.overwrite(dest_id)
        except curses.error:
            return ERR
    else:
        return pdlib.overwrite(src_id, dest_id)

def pair_content(pair_number):
    if NCURSES:
        try:
            return curses.pair_content(pair_number)
        except curses.error:
            return ERR
    else:
        fg=ctypes.c_short()
        bg=ctypes.c_short()
        pdlib.pair_content(pair_number, ctypes.byref(fg), ctypes.byref(bg))
        return (fg.value, bg.value)

def pair_number(attr):
    if NCURSES:
        try:
            return curses.pair_number(attr)
        except curses.error:
            return ERR
    else:
        return PD_PAIR_NUMBER(attr)

def prefresh(scr_id, pminrow, pmincol, sminrow, smincol, smaxrow, smaxcol):
    if NCURSES:
        try:
            return scr_id.refresh(pminrow, pmincol, sminrow, smincol, smaxrow, smaxcol)
        except curses.error:
            return ERR
    else:
        return pdlib.prefresh(scr_id, pminrow, pmincol, sminrow, smincol, smaxrow, smaxcol)

def putp(cstring):
    if NCURSES:
        try:
            return curses.putp(cstring)
        except curses.error:
            return ERR
    else:
        return pdlib.putp(CSTR(cstring))

def putwin(scr_id, file):    # THIS IS NOT CROSS-PLATFORM YET, AVOID IF POSSIBLE
    if NCURSES:
        try:
            return scr_id.putwin(file)
        except curses.error:
            return ERR
    else:
        raise Exception("UNICURSES_PUTWIN: 'putwin' is unavailable under Windows!")

def qiflush():
    if NCURSES:
        try:
            return curses.qiflush()
        except curses.error:
            return ERR
    else:
        return pdlib.qiflush()

def raw():
    if NCURSES:
        try:
            return curses.raw()
        except curses.error:
            return ERR
    else:
        return pdlib.raw()

def wredrawln(scr_id, beg, num):
    if NCURSES:
        try:
            return scr_id.redrawln(beg, num)
        except curses.error:
            return ERR
    else:
        return pdlib.wredrawln(scr_id, beg, num)

def redrawwin(scr_id):
    if NCURSES:
        try:
            return scr_id.redrawwin()
        except curses.error:
            return ERR
    else:
        return pdlib.redrawwin(scr_id)

def wrefresh(scr_id):
    if NCURSES:
        try:
            return scr_id.refresh()
        except curses.error:
            return ERR
    else:
        return pdlib.wrefresh(scr_id)

def reset_prog_mode():
    if NCURSES:
        try:
            return curses.reset_prog_mode()
        except curses.error:
            return ERR
    else:
        return pdlib.reset_prog_mode()

def reset_shell_mode():
    if NCURSES:
        try:
            return curses.reset_shell_mode()
        except curses.error:
            return ERR
    else:
        return pdlib.reset_shell_mode()

def wscrl(scr_id, lines=1):
    if NCURSES:
        try:
            return scr_id.scroll(lines)
        except curses.error:
            return ERR
    else:
        return pdlib.wscrl(scr_id, lines)

def scrollok(scr_id, flag):
    if NCURSES:
        try:
            return scr_id.scrollok(flag)
        except curses.error:
            return ERR
    else:
        return pdlib.scrollok(scr_id, flag)

def wsetscrreg(scr_id, top, bottom):
    if NCURSES:
        try:
            return scr_id.setscrreg(top, bottom)
        except curses.error:
            return ERR
    else:
        return pdlib.wsetscrreg(scr_id, top, bottom)

def setsyx(y, x):
    global PDC_LEAVEOK
    if NCURSES:
        try:
            return curses.setsyx(y, x)
        except curses.error:
            return ERR
    else:
        curscr = PD_GET_CURSCR()
        if y == x == -1:
            PDC_LEAVEOK = True
        else:
            PDC_LEAVEOK = False
        return pdlib.setsyx(y, x)

def setupterm(termstr, fd):
    if NCURSES:
        try:
            return curses.setupterm(termstr, fd)
        except curses.error:
            return ERR
    else:
        return pdlib.setupterm(termstr, fd, None)

def wstandend(scr_id):
    if NCURSES:
        try:
            return scr_id.standend()
        except curses.error:
            return ERR
    else:
        return pdlib.wstandend(scr_id)

def wstandout(scr_id):
    if NCURSES:
        try:
            return scr_id.standout()
        except curses.error:
            return ERR
    else:
        return pdlib.wstandout(scr_id)

def start_color():
    if NCURSES:
        try:
            return curses.start_color()
        except curses.error:
            return ERR
    else:
        return pdlib.start_color()

def subpad(scrwin, nlines, ncols, begin_y, begin_x):
    if NCURSES:
        try:
            return scrwin.subpad(nlines, ncols, begin_y, begin_x)
        except curses.error:
            return ERR
    else:
        pdlib.subpad.restype = ctypes.c_void_p
        return ctypes.c_void_p(pdlib.subpad(scrwin, nlines, ncols, begin_y, begin_x))

def subwin(srcwin, nlines, ncols, begin_y, begin_x):
    if NCURSES:
        try:
            return srcwin.subwin(nlines, ncols, begin_y, begin_x)
        except curses.error:
            return ERR
    else:
        pdlib.subwin.restype = ctypes.c_void_p
        return ctypes.c_void_p(pdlib.subwin(srcwin, nlines, ncols, begin_y, begin_x))

def wsyncdown(scr_id):
    if NCURSES:
        try:
            return scr_id.syncdown()
        except curses.error:
            return ERR
    else:
        return pdlib.wsyncdown(scr_id)

def syncok(scr_id, flag):
    if NCURSES:
        try:
            return scr_id.syncok(flag)
        except curses.error:
            return ERR
    else:
        return pdlib.syncok(scr_id, flag)

def wsyncup(scr_id):
    if NCURSES:
        try:
            return scr_id.syncup()
        except curses.error:
            return ERR
    else:
        return pdlib.wsyncup(scr_id)

def termattrs():
    if NCURSES:
        try:
            return curses.termattrs()
        except curses.error:
            return ERR
    else:
        return pdlib.termattrs()

def termname():
    if NCURSES:
        try:
            return curses.termname()
        except curses.error:
            return ERR
    else:
        return pdlib.termname().decode()

def tigetflag(capname):
    if NCURSES:
        try:
            return curses.tigetflag(capname)
        except curses.error:
            return ERR
    else:
        return pdlib.tigetflag(CSTR(capname))

def tigetnum(capname):
    if NCURSES:
        try:
            return curses.tigetnum(capname)
        except curses.error:
            return ERR
    else:
        return pdlib.tigetnum(CSTR(capname))

def tigetstr(capname):
    if NCURSES:
        try:
            return curses.tigetstr(capname)
        except curses.error:
            return ERR
    else:
        return pdlib.tigetstr(CSTR(capname))

def wtimeout(scr_id, delay):
    if NCURSES:
        try:
            return scr_id.timeout(delay)
        except curses.error:
            return ERR
    else:
        return pdlib.wtimeout(scr_id, delay)

def wtouchline(scr_id, start, count, changed=1):
    if NCURSES:
        try:
            return scr_id.touchline(start, count, changed)
        except curses.error:
            return ERR
    else:
        return pdlib.wtouchln(scr_id, start, count, changed)

def touchwin(scr_id):
    if NCURSES:
        try:
            return scr_id.touchwin()
        except curses.error:
            return ERR
    else:
        return pdlib.touchwin(scr_id)

def tparm(str, p1=0, p2=0, p3=0, p4=0, p5=0, p6=0, p7=0, p8=0, p9=0):
    if NCURSES:
        try:
            return curses.tparm(str, p1, p2, p3, p4, p5, p6, p7, p8, p9)
        except curses.error:
            return ERR
    else:
        return pdlib.tparm(CSTR(str), p1, p2, p3, p4, p5, p6, p7, p8, p9)

def typeahead(fd):
    if NCURSES:
        try:
            return curses.typeahead(fd)
        except curses.error:
            return ERR
    else:
        return pdlib.typeahead(fd)

def wvline(scr_id, ch, n):
    if NCURSES:
        try:
            return scr_id.vline(ch, n)
        except curses.error:
            return ERR
    else:
        return pdlib.wvline(scr_id, ch, n)

def unctrl(ch):
    if NCURSES:
        try:
            return curses.unctrl(ch)
        except curses.error:
            return ERR
    else:
        return pdlib.unctrl(ch)

def ungetch(ch):
    if NCURSES:
        try:
            return curses.ungetch(ch)
        except curses.error:
            return ERR
    else:
        return pdlib.PDC_ungetch(ch)

def ungetmouse(id, x, y, z, bstate):
    if NCURSES:
        try:
            return curses.ungetmouse(id, x, y, z, bstate)
        except curses.error:
            return ERR
    else:
        m_event = MEVENT()
        m_event.id = id
        m_event.x = x
        m_event.y = y
        m_event.z = z
        m_event.mmask_t = bstate
        return pdlib.ungetmouse(ctypes.byref(m_event))

def untouchwin(scr_id):
    if NCURSES:
        try:
            return scr_id.untouchwin()
        except curses.error:
            return ERR
    else:
        return pdlib.untouchwin(scr_id)

def use_default_colors():
    if NCURSES:
        try:
            return curses.use_default_colors()
        except curses.error:
            return ERR
    else:
        return pdlib.use_default_colors()

def use_env(flag):
    if NCURSES:
        try:
            return curses.use_env(flag)
        except curses.error:
            return ERR
    else:
        return pdlib.use_env(flag)

# ++ REGULAR FUNCTIONS THAT DO NOT TAKE A WINDOW AS AN ARGUMENT ++

def attroff(attr): return wattroff(stdscr, attr)
def attron(attr): return wattron(stdscr, attr)
def attrset(attr): return wattrset(stdscr, attr)
def clear(): return wclear(stdscr)
def getch(): return wgetch(stdscr)
def mvinsnstr(y, x, str, n, attr="NO_USE"): return mvwinsnstr(stdscr, y, x, str, n, attr)
def insnstr(str, n, attr="NO_USE"): return winsnstr(stdscr, str, n, attr)
def insch(ch, attr=A_NORMAL): return winsch(stdscr, ch, attr)
def refresh(): return wrefresh(stdscr)
def border(ls=ACS_VLINE, rs=ACS_VLINE, ts=ACS_HLINE, bs=ACS_HLINE, tl=ACS_ULCORNER, tr=ACS_URCORNER, bl=ACS_LLCORNER, br=ACS_LRCORNER): return wborder(stdscr, ls, rs, ts, bs, tl, tr, bl, br)
def bkgd(ch, attr=A_NORMAL): return wbkgd(stdscr, ch, attr)
def bkgdset(ch, attr=A_NORMAL): return wbkgdset(stdscr, ch, attr)
def erase(): return werase(stdscr)
def timeout(delay): return wtimeout(stdscr, delay)
def hline(ch, n): return whline(stdscr, ch, n)
def vline(ch, n): return wvline(stdscr, ch, n)
def mvhline(y, x, ch, n): return mvwhline(stdscr, y, x, ch, n)
def mvvline(y, x, ch, n): return mvwvline(stdscr, y, x, ch, n)
def scroll(lines=1): return wscrl(stdscr, lines)
def setscrreg(top, bottom): return wsetscrreg(stdscr, top, bottom)
def delch(): return wdelch(stdscr)
def mvdelch(y, x): return mvwdelch(stdscr, y, x)
def move(new_y, new_x): return wmove(stdscr, new_y, new_x)
def insertln(): return winsertln(stdscr)
def insdelln(nlines): return winsdelln(stdscr, nlines)
def inch(): return winch(stdscr)
def mvinch(y, x): return mvwinch(stdscr, y, x)
def clrtobot(): return wclrtobot(stdscr)
def clrtoeol(): return wclrtoeol(stdscr)
def mvgetch(y, x): return mvwgetch(stdscr, y, x)
def addch(ch, attr=A_NORMAL): return waddch(stdscr, ch, attr)
def mvaddch(y, x, ch, attr=A_NORMAL): return mvwaddch(stdscr, y, x, ch, attr)
def addstr(cstr, attr="NO_USE"): return waddstr(stdscr, cstr, attr)
def mvaddstr(y, x, cstr, attr="NO_USE"): return mvwaddstr(stdscr, y, x, cstr, attr)
def addnstr(cstr, n, attr="NO_USE"): return waddnstr(stdscr, cstr, n, attr)
def mvaddnstr(y, x, cstr, n, attr="NO_USE"): return mvwaddnstr(stdscr, y, x, cstr, n, attr)
def insstr(cstr, attr="NO_USE"): return winsstr(stdscr, cstr, attr)
def mvinsstr(y, x, cstr, attr="NO_USE"): return mvwinsstr(stdscr, y, x, cstr, attr)
def echochar(ch, attr=A_NORMAL): return wechochar(stdscr, ch, attr)
def standout(): return wstandout(stdscr)
def standend(): return wstandend(stdscr)
def chgat(num, attr, color, opts=None): return wchgat(stdscr, num, attr, color, opts)
def mvchgat(y, x, num, attr, color, opts=None): return mvwchgat(stdscr, y, x, num, attr, color, opts)
def deleteln(): return wdeleteln(stdscr)
def mvdeleteln(y, x): return mvwdeleteln(stdscr, y, x)
def enclose(y, x): return wenclose(stdscr, y, x)
def getstr(): return wgetstr(stdscr)
def mvgetstr(y, x): return mvwgetstr(stdscr, y, x)
def instr(n=-1): return winstr(stdscr, n)
def mvinstr(y, x, n=-1): return mvwinstr(stdscr, y, x, n)
def touchline(y, x, changed=1): return wtouchline(stdscr, y, x, changed)
def touchln(y, x, changed=1): return wtouchline(stdscr, y, x, changed)
def mvinsch(y, x, ch, attr=A_NORMAL): return mvwinsch(stdscr, y, x, ch, attr)
def redrawln(beg, num): return wredrawln(stdscr, beg, num)
def syncdown(): return wsyncdown(stdscr)
def syncup(): return wsyncup(stdscr)
def getkey(y=-1, x=-1): return wgetkey(stdscr, y, x)

# ++ UNIFIED CURSES: PANEL MODULE ++

def panel_above(pan_id):
    if NCURSES:
        try:
            return pan_id.above()
        except curses.panel.error:
            return ERR
    else:
        return pdlib.panel_above(pan_id)

def panel_below(pan_id):
    if NCURSES:
        try:
            return pan_id.below()
        except curses.panel.error:
            return ERR
    else:
        return pdlib.panel_below(pan_id)

def bottom_panel(pan_id):
    if NCURSES:
        try:
            return pan_id.bottom()
        except curses.panel.error:
            return ERR
    else:
        return pdlib.bottom_panel(pan_id)

def del_panel(pan_id):
    if NCURSES:
        try:
            del(pan_id)
            return OK
        except curses.panel.error:
            return ERR
    else:
        return pdlib.del_panel(pan_id)

def panel_hidden(pan_id):
    if NCURSES:
        try:
            return pan_id.hidden()
        except curses.panel.error:
            return ERR
    else:
        mode = pdlib.panel_hidden(pan_id)
        if mode == OK: return True
        return False

def hide_panel(pan_id):
    if NCURSES:
        try:
            return pan_id.hide()
        except curses.panel.error:
            return ERR
    else:
        return pdlib.hide_panel(pan_id)

def move_panel(pan_id, y, x):
    if NCURSES:
        try:
            return pan_id.move(y, x)
        except curses.panel.error:
            return ERR
    else:
        return pdlib.move_panel(pan_id, y, x)

def new_panel(scr_id):
    if NCURSES:
        try:
            return curses.panel.new_panel(scr_id)
        except curses.panel.error:
            return ERR
    else:
        return pdlib.new_panel(scr_id)

def replace_panel(pan_id, win):
    if NCURSES:
        try:
            return pan_id.replace(win)
        except curses.panel.error:
            return ERR
    else:
        return pdlib.replace_panel(pan_id, win)

def set_panel_userptr(pan_id, obj):
    if NCURSES:
        try:
            return pan_id.set_userptr(obj)
        except curses.panel.error:
            return ERR
    else:
        return pdlib.set_panel_userptr(pan_id, obj)

def show_panel(pan_id):
    if NCURSES:
        try:
            return pan_id.show()
        except curses.panel.error:
            return ERR
    else:
        return pdlib.show_panel(pan_id)

def top_panel(pan_id):
    if NCURSES:
        try:
            return pan_id.top()
        except curses.panel.error:
            return ERR
    else:
        return pdlib.top_panel(pan_id)

def update_panels():
    if NCURSES:
        try:
            return curses.panel.update_panels()
        except curses.panel.error:
            return ERR
    else:
        return pdlib.update_panels()

def panel_userptr(pan_id):
    if NCURSES:
        try:
            return pan_id.userptr()
        except curses.panel.error:
            return ERR
    else:
        return pdlib.panel_userptr(pan_id)

def panel_window(pan_id):
    if NCURSES:
        try:
            return pan_id.window()
        except curses.panel.error:
            return ERR
    else:
        return pdlib.panel_window(pan_id)

# --- UNIFIED CURSES ---
