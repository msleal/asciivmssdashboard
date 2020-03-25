#!/usr/bin/env python
# Draw World Map in UniCurses...

"""
Copyright (c) 2016, Marcelo Leal
Description: The power is in the terminal...
License: MIT (see LICENSE.txt file for details)
"""

from unicurses import *
from windows import *

def draw_map(window, continent):
	#Draw North and Central America Continents...
	if (continent == "northandcentralamerica"):
		draw_line(window, 0, 48, 6, ACS_HLINE); draw_line(window, 0, 69, 8, ACS_HLINE); draw_line(window, 1, 45, 11, ACS_HLINE); draw_line(window, 1, 60, 5, ACS_HLINE); 
		draw_line(window, 1, 66, 13, ACS_HLINE); draw_line(window, 1, 81, 2, ACS_HLINE); draw_line(window, 2, 40, 3, ACS_HLINE); draw_line(window, 2, 47, 6, ACS_HLINE);
		draw_line(window, 2, 55, 27, ACS_HLINE); draw_line(window, 3, 31, 1, ACS_HLINE); draw_line(window, 3, 35, 2, ACS_HLINE); draw_line(window, 3, 38, 1, ACS_HLINE);
		draw_line(window, 3, 41, 3, ACS_HLINE); draw_line(window, 3, 45, 5, ACS_HLINE); draw_line(window, 3, 53, 27, ACS_HLINE); draw_line(window, 4, 26, 2, ACS_HLINE);
		draw_line(window, 4, 39, 3, ACS_HLINE); draw_line(window, 4, 43, 6, ACS_HLINE); draw_line(window, 4, 54, 27, ACS_HLINE); draw_line(window, 5, 30, 1, ACS_HLINE);
		draw_line(window, 5, 39, 1, ACS_HLINE); draw_line(window, 5, 43, 4, ACS_HLINE); draw_line(window, 5, 60, 20, ACS_HLINE); draw_line(window, 6, 24, 2, ACS_HLINE);
		draw_line(window, 6, 28, 4, ACS_HLINE); draw_line(window, 6, 33, 1, ACS_HLINE); draw_line(window, 6, 37, 1, ACS_HLINE); draw_line(window, 6, 40, 1, ACS_HLINE);
		draw_line(window, 6, 43, 1, ACS_HLINE); draw_line(window, 6, 45, 2, ACS_HLINE); draw_line(window, 6, 48, 1, ACS_HLINE); draw_line(window, 6, 61, 18, ACS_HLINE);
		draw_line(window, 7, 4, 7, ACS_HLINE); draw_line(window, 7, 21, 1, ACS_HLINE); draw_line(window, 7, 30, 6, ACS_HLINE); draw_line(window, 7, 39, 2, ACS_HLINE);
		draw_line(window, 7, 44, 10, ACS_HLINE); draw_line(window, 7, 62, 15, ACS_HLINE); draw_line(window, 8, 2, 27, ACS_HLINE); draw_line(window, 8, 33, 3, ACS_HLINE);
		draw_line(window, 8, 38, 1, ACS_HLINE); draw_line(window, 8, 40, 3, ACS_HLINE); draw_line(window, 8, 45, 2, ACS_HLINE); draw_line(window, 8, 50, 1, ACS_HLINE);
		draw_line(window, 8, 52, 3, ACS_HLINE); draw_line(window, 8, 63, 11, ACS_HLINE); draw_line(window, 9, 1, 43, ACS_HLINE); draw_line(window, 9, 51, 3, ACS_HLINE);
		draw_line(window, 9, 56, 1, ACS_HLINE); draw_line(window, 9, 63, 7, ACS_HLINE); draw_line(window, 9, 78, 5, ACS_HLINE); draw_line(window, 10, 3, 39, ACS_HLINE);
		draw_line(window, 10, 49, 1, ACS_HLINE); draw_line(window, 10, 64, 4, ACS_HLINE); draw_line(window, 10, 79, 3, ACS_HLINE); draw_line(window, 11, 2, 38, ACS_HLINE);
		draw_line(window, 11, 50, 3, ACS_HLINE); draw_line(window, 11, 66, 2, ACS_HLINE); draw_line(window, 12, 6, 1, ACS_HLINE); draw_line(window, 12, 19, 22, ACS_HLINE);
		draw_line(window, 12, 50, 8, ACS_HLINE); draw_line(window, 13, 2, 1, ACS_HLINE); draw_line(window, 13, 20, 26, ACS_HLINE); draw_line(window, 13, 48, 12, ACS_HLINE);
		draw_line(window, 14, 22, 25, ACS_HLINE); draw_line(window, 14, 49, 11, ACS_HLINE); draw_line(window, 15, 24, 32, ACS_HLINE); draw_line(window, 15, 60, 2, ACS_HLINE);
		draw_line(window, 16, 24, 30, ACS_HLINE); draw_line(window, 16, 57, 1, ACS_HLINE); draw_line(window, 17, 24, 28, ACS_HLINE); draw_line(window, 18, 25, 25, ACS_HLINE);
		draw_line(window, 19, 26, 24, ACS_HLINE); draw_line(window, 20, 28, 19, ACS_HLINE); draw_line(window, 21, 30, 1, ACS_HLINE); draw_line(window, 21, 33, 5, ACS_HLINE);
		draw_line(window, 21, 47, 1, ACS_HLINE); draw_line(window, 22, 32, 1, ACS_HLINE); draw_line(window, 22, 34, 4, ACS_HLINE); draw_line(window, 22, 48, 1, ACS_HLINE);
		draw_line(window, 23, 35, 4, ACS_HLINE); draw_line(window, 23, 42, 1, ACS_HLINE); draw_line(window, 23, 52, 1, ACS_HLINE); draw_line(window, 24, 40, 6, ACS_HLINE);
		draw_line(window, 25, 45, 1, ACS_HLINE);
	elif (continent == "southamerica"):
		#Draw South America Continent...
		draw_line(window, 0, 4, 3, ACS_HLINE); draw_line(window, 1, 3, 9, ACS_HLINE); draw_line(window, 2, 3, 13, ACS_HLINE); draw_line(window, 3, 1, 17, ACS_HLINE);
		draw_line(window, 4, 1, 22, ACS_HLINE); draw_line(window, 5, 2, 23, ACS_HLINE); draw_line(window, 6, 3, 21, ACS_HLINE); draw_line(window, 7, 6, 17, ACS_HLINE);
		draw_line(window, 8, 7, 15, ACS_HLINE); draw_line(window, 9, 6, 12, ACS_HLINE); draw_line(window, 10, 6, 12, ACS_HLINE); draw_line(window, 11, 6, 9, ACS_HLINE);
		draw_line(window, 12, 5, 8, ACS_HLINE); draw_line(window, 13, 5, 5, ACS_HLINE); draw_line(window, 14, 4, 5, ACS_HLINE); draw_line(window, 15, 4, 4, ACS_HLINE);
		draw_line(window, 16, 4, 3, ACS_HLINE); draw_line(window, 17, 4, 3, ACS_HLINE); draw_line(window, 17, 11, 1, ACS_HLINE); draw_line(window, 18, 5, 3, ACS_HLINE);
	elif (continent == "africa"):
		#Draw Africa Continent...
		draw_line(window, 0, 4, 5, ACS_HLINE); draw_line(window, 0, 24, 11, ACS_HLINE); draw_line(window, 1, 5, 9, ACS_HLINE); draw_line(window, 2, 3, 14, ACS_HLINE);
 		#Middle East
		draw_line(window, 1, 29, 9, ACS_HLINE); draw_line(window, 2, 20, 18, ACS_HLINE); draw_line(window, 3, 29, 7, ACS_HLINE); draw_line(window, 4, 30, 8, ACS_HLINE);
		draw_line(window, 5, 31, 7, ACS_HLINE); draw_line(window, 6, 32, 5, ACS_HLINE); draw_line(window, 3, 2, 25, ACS_HLINE); draw_line(window, 4, 1, 27, ACS_HLINE);
		draw_line(window, 5, 1, 28, ACS_HLINE); draw_line(window, 6, 1, 29, ACS_HLINE); draw_line(window, 7, 1, 31, ACS_HLINE); draw_line(window, 7, 34, 2, ACS_HLINE);
		draw_line(window, 8, 3, 33, ACS_HLINE); draw_line(window, 9, 4, 5, ACS_HLINE); draw_line(window, 9, 14, 20, ACS_HLINE); draw_line(window, 10, 14, 18, ACS_HLINE);
		draw_line(window, 11, 15, 15, ACS_HLINE); draw_line(window, 12, 16, 14, ACS_HLINE); draw_line(window, 13, 16, 15, ACS_HLINE); draw_line(window, 14, 16, 13, ACS_HLINE);
		draw_line(window, 15, 17, 11, ACS_HLINE); draw_line(window, 16, 17, 11, ACS_HLINE); draw_line(window, 17, 18, 8, ACS_HLINE); draw_line(window, 18, 19, 5, ACS_HLINE);
        	#Island...
		draw_line(window, 13, 35, 1, ACS_HLINE); draw_line(window, 14, 33, 3, ACS_HLINE); draw_line(window, 15, 33, 2, ACS_HLINE); draw_line(window, 16, 33, 2, ACS_HLINE);
	elif (continent == "oceania"):
		#Draw Oceania Continent...
		draw_line(window, 0, 2, 1, ACS_HLINE); draw_line(window, 0, 5, 1, ACS_HLINE); draw_line(window, 0, 11, 3, ACS_HLINE); draw_line(window, 1, 4, 2, ACS_HLINE);
		draw_line(window, 1, 9, 4, ACS_HLINE); draw_line(window, 2, 6, 1, ACS_HLINE); draw_line(window, 2, 24, 4, ACS_HLINE); draw_line(window, 3, 11, 1, ACS_HLINE);
		draw_line(window, 3, 26, 2, ACS_HLINE); draw_line(window, 4, 21, 2, ACS_HLINE); draw_line(window, 4, 27, 1, ACS_HLINE); draw_line(window, 5, 17, 8, ACS_HLINE);
		draw_line(window, 5, 27, 2, ACS_HLINE); draw_line(window, 6, 14, 16, ACS_HLINE); draw_line(window, 7, 12, 20, ACS_HLINE); draw_line(window, 8, 12, 21, ACS_HLINE);
		draw_line(window, 9, 13, 19, ACS_HLINE); draw_line(window, 10, 13, 2, ACS_HLINE); draw_line(window, 10, 26, 5, ACS_HLINE); draw_line(window, 10, 44, 1, ACS_HLINE);
		draw_line(window, 11, 44, 2, ACS_HLINE); draw_line(window, 12, 29, 1, ACS_HLINE); draw_line(window, 12, 43, 1, ACS_HLINE); draw_line(window, 13, 41, 1, ACS_HLINE);
	else:
		#Draw Europe and Asia Continents...
		draw_line(window, 0, 15, 3, ACS_HLINE); draw_line(window, 0, 55, 3, ACS_HLINE); draw_line(window, 1, 12, 5, ACS_HLINE); draw_line(window, 1, 57, 2, ACS_HLINE);
		draw_line(window, 1, 60, 1, ACS_HLINE); draw_line(window, 2, 13, 2, ACS_HLINE); draw_line(window, 2, 41, 1, ACS_HLINE); draw_line(window, 2, 60, 2, ACS_HLINE);
		draw_line(window, 3, 36, 2, ACS_HLINE); draw_line(window, 3, 53, 12, ACS_HLINE); draw_line(window, 3, 79, 4, ACS_HLINE); draw_line(window, 3, 85, 2, ACS_HLINE);
		draw_line(window, 4, 34, 2, ACS_HLINE); draw_line(window, 4, 42, 2, ACS_HLINE); draw_line(window, 4, 49, 25, ACS_HLINE); draw_line(window, 4, 80, 2, ACS_HLINE);
		draw_line(window, 5, 35, 1, ACS_HLINE); draw_line(window, 5, 18, 3, ACS_HLINE); draw_line(window, 5, 41, 3, ACS_HLINE); draw_line(window, 5, 46, 45, ACS_HLINE);
		draw_line(window, 5, 102, 1, ACS_HLINE); draw_line(window, 6, 14, 12, ACS_HLINE); draw_line(window, 6, 33, 11, ACS_HLINE); draw_line(window, 6, 46, 57, ACS_HLINE);
		draw_line(window, 7, 28, 79, ACS_HLINE); draw_line(window, 7, 12, 11, ACS_HLINE); draw_line(window, 8, 10, 5, ACS_HLINE); draw_line(window, 8, 17, 84, ACS_HLINE);
		draw_line(window, 8, 106, 1, ACS_HLINE); draw_line(window, 9, 8, 6, ACS_HLINE); draw_line(window, 9, 17, 72, ACS_HLINE); draw_line(window, 9, 93, 4, ACS_HLINE);
		draw_line(window, 10, 2, 1, ACS_HLINE); draw_line(window, 10, 12, 2, ACS_HLINE); draw_line(window, 10, 18, 63, ACS_HLINE); draw_line(window, 10, 90, 2, ACS_HLINE);
		draw_line(window, 11, 3, 1, ACS_HLINE); draw_line(window, 11, 10, 1, ACS_HLINE); draw_line(window, 11, 16, 62, ACS_HLINE); draw_line(window, 11, 89, 3, ACS_HLINE);
		draw_line(window, 12, 0, 2, ACS_HLINE); draw_line(window, 12, 3, 2, ACS_HLINE); draw_line(window, 12, 7, 74, ACS_HLINE); draw_line(window, 12, 82, 1, ACS_HLINE);
		draw_line(window, 12, 89, 1, ACS_HLINE); draw_line(window, 13, 0, 3, ACS_HLINE); draw_line(window, 13, 4, 2, ACS_HLINE); draw_line(window, 13, 7, 74, ACS_HLINE);
		draw_line(window, 13, 82, 1, ACS_HLINE); draw_line(window, 14, 5, 16, ACS_HLINE); draw_line(window, 14, 23, 1, ACS_HLINE); draw_line(window, 14, 26, 4, ACS_HLINE);
		draw_line(window, 14, 34, 45, ACS_HLINE); draw_line(window, 14, 82, 1, ACS_HLINE); draw_line(window, 15, 1, 5, ACS_HLINE); draw_line(window, 15, 12, 1, ACS_HLINE);
		draw_line(window, 15, 16, 4, ACS_HLINE); draw_line(window, 15, 23, 2, ACS_HLINE); draw_line(window, 15, 28, 3, ACS_HLINE); draw_line(window, 15, 34, 41, ACS_HLINE);
		draw_line(window, 15, 80, 3, ACS_HLINE); draw_line(window, 16, 34, 34, ACS_HLINE); draw_line(window, 16, 73, 1, ACS_HLINE); draw_line(window, 16, 79, 2, ACS_HLINE);
		draw_line(window, 17, 34, 36, ACS_HLINE); draw_line(window, 17, 73, 1, ACS_HLINE); draw_line(window, 17, 78, 2, ACS_HLINE); draw_line(window, 18, 34, 37, ACS_HLINE);
		draw_line(window, 19, 34, 36, ACS_HLINE); draw_line(window, 20, 34, 3, ACS_HLINE); draw_line(window, 20, 42, 25, ACS_HLINE); draw_line(window, 20, 70, 1, ACS_HLINE);
		draw_line(window, 21, 34, 2, ACS_HLINE); draw_line(window, 21, 45, 6, ACS_HLINE); draw_line(window, 21, 55, 7, ACS_HLINE); draw_line(window, 22, 45, 3, ACS_HLINE);
		draw_line(window, 22, 57, 6, ACS_HLINE); draw_line(window, 22, 70, 1, ACS_HLINE); draw_line(window, 23, 46, 2, ACS_HLINE); draw_line(window, 23, 58, 1, ACS_HLINE);
		draw_line(window, 23, 61, 3, ACS_HLINE); draw_line(window, 24, 48, 1, ACS_HLINE); draw_line(window, 24, 58, 1, ACS_HLINE); draw_line(window, 24, 72, 1, ACS_HLINE);
