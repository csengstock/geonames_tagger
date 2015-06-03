#!/usr/bin/python

import sys
try:
    from triedict import TrieDict
except ImportError, e:
    sys.path.append("../extlib")
    sys.path.append("./extlib")
    from triedict import TrieDict


def create_triedict(fn_name2IDs, fn_output, max_n=-1):
    td = TrieDict()
    fp_name2IDs = open(fn_name2IDs, "r")
    sys.stderr.write("creating trie...\n")
    for i,line in enumerate(fp_name2IDs):
        if max_n > 0 and i >= max_n:
            break
        if i % 1000 == 0:
            sys.stderr.write("\r%d" % i)
            sys.stderr.flush()
        line = line.strip()
        name, IDs = line.split("\t")
        name = name.decode("utf-8")
        td.add_pattern(name, i)
    sys.stderr.write("\ncreating suffix pointers...\n")
    td.generate_suffix_pointers()
    sys.stderr.write("\nsaving trie...\n")
    td.save(fn_output)
    sys.stderr.write("done\n")

if __name__ == "__main__":
    create_triedict("../idx/name2ID.tsv", "../idx/trie.bin")
