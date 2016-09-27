# -*- coding: utf-8 -*-
"""
Created on Wed Sep 21 16:27:16 2016

@author: Yiting
"""

"""
MAIN PROGRAM
"""

import os


# go to main folder
main_folder = "F:/fresno_sample"
os.chdir(main_folder)

# check folder
retval = os.getcwd()
print "Current working directory %s" % retval

# parse folder name under main folder
