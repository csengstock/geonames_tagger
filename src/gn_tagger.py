#!/usr/bin/python

import sys
from gn_index import GeonamesIndex, load_IDs
from gn_trie import TrieDict

out = sys.stderr.write

class GNTagger:
    def __init__(self, fn_geonames, fn_trie, fn_value2IDs):
        out("loading geonames index...\n")
        self.gn_index = GeonamesIndex(fn_geonames)
        out("loading trie...\n")
        self.trie = TrieDict.load(fn_trie)
        out("loading value2IDs list...\n")
        self.value2IDs = load_IDs(fn_value2IDs)
        out("done\n")

    def parse(self, text):
        text = text.strip().decode("utf-8")
        matches = self.trie.match(text, bound_chars=" .,;:_-!?=()[]{}'\"$%&")
        result = {"success": 1, "n_matches": len(matches), "matches": []}
        for match in matches:
            key, value, pos = match
            result["matches"].append({})
            rec = result["matches"][-1]
            rec["idx"] = (pos-len(key)+1, pos), 
            rec["token"] = key 
            rec["gnrecs"] = []
            IDs = [int(ID) for ID in self.value2IDs[value].split(",")]
            for ID in IDs:
                gnrec = self.gn_index.get(ID)
                rec["gnrecs"].append(gnrec.split("\t"))
        return result

if __name__ == "__main__":
    gt = GNTagger("../data/allCountries.txt", "../idx01/trie.bin", "../idx01/name2ID.tsv")
    raw_input("hit")
    s = "this is a text about heidelberg in germany dude! Have fun and hang loose!!!"
    result = gt.parse(s)
    print result
    import json
    print json.dumps(result)
