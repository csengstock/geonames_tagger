#!/usr/bin/python

import sys
sys.path.append("./src")
import os
from gn_index import create_name2ID_file
from gn_trie import create_triedict

def usage():
    print """Usage:  gnt_index.py IN_FILE OUT_FOLDER [MAX_N]
   
    IN_FILE:    Path to the 'allCountries.txt' file (download form genonames)
    OUT_FOLDER: Folder path where the index gets generated. Path must not exist already!
    MAX_N:      Only use top MAX_N rows of IN_FILE (usefull for debugging; optional).
"""
    sys.exit(1)

def create_index(fn_in, path_out, max_n):
    print "creating index in '%s'" % path_out
    os.mkdir(path_out)
    print "creating name2ID.tsv"
    create_name2ID_file(fn_in, path_out+"/name2ID.tsv", max_n)
    create_triedict(path_out+"/name2ID.tsv", path_out+"/trie.bin")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        usage()

    fn_in = sys.argv[1]
    path_out = sys.argv[2].rstrip("/")
    max_n = -1
    if not os.path.exists(fn_in):
        print "IN_FILE not found!"
        print "--"
        usage()
    if os.path.exists(path_out):
        print "OUT_FOLDER already exist. Choose another folder name!"
        print "--"
        usage()
    if len(sys.argv) == 4:
        max_n = int(sys.argv[3])
    print "INPUT: ", fn_in
    print "OUTPUT:", path_out
    print "MAX_N: ", max_n
    create_index(fn_in, path_out, max_n)
