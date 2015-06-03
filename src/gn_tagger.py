# geonames tagger
#
# Copyright (c) 2015 Christian Sengstock, All rights reserved.
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 3.0 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library.

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

    def parse(self, text, bound_chars):
        text = text.strip().decode("utf-8")
        # bound_chars = " .,;:_-!?=()[]{}'\"$%&"
        matches = self.trie.match(text, bound_chars=bound_chars)
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
