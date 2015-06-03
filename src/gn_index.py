
#!/usr/bin/python

import sys

def _all_countries_scanner(fn, callback, max_n=1):
    """
    Scans the 'allCountries.txt' file and calls
    the callback for each record.
    """
    fp = open(fn, "r")
    for i,line in enumerate(fp):
        if max_n > 0 and i >= max_n:
            break
        if i % 1000 == 0:
            sys.stderr.write("\r%d" % i)
            sys.stderr.flush()
        callback(line.strip())
    sys.stderr.write("\n")
    fp.close()

class GeonamesIndex:
    """
    A simple geonames ID based index on the
    geonames records (lines in allCountries.txt).
    
    Needs ~1795 MB of RAM for all records.
    """
    def __init__(self, fn, max_n=-1):
        """
        Creates the index.
        Args:
            fn: Path to the 'allCountries.txt' file
            max_n: Only index the first max_n records.
                Defaults to -1 (= all records).
        """
        self.ID2rec = {}
        def callback(line):
            attrs = line.split("\t")
            ID = int(attrs[0])
            self.ID2rec[ID] = line
        _all_countries_scanner(fn, callback, max_n)

    def get(self, ID):
        try:
            return self.ID2rec[ID]
        except KeyError, e:
            return None

def create_name2ID_file(fn_input, fn_output, max_n=-1):
    """
    Creates the name2ID file mapping all geonames
    (primary and alternate) to their IDs. This
    file is needed by the Aho-Corasick pattern matcher.
    
    Needs ~4.9GB of RAM. Can be reduced to ~3.5 GB 
    by using external sort (e.g. linux sort)
    """
    name2ID = {}
    def callback(line):
        attrs = line.split("\t")
        ID = int(attrs[0])
        pname = attrs[1].strip().lower()
        sname = attrs[2].strip().lower()
        anames = [aname.strip().lower() for aname in attrs[3].split(",")]
        anames.append(pname)
        anames.append(sname)
        anames = set(anames)
        for name in anames:
            if name != "":
                name2ID.setdefault(name, set())
                name2ID[name].add(ID)
    _all_countries_scanner(fn_input, callback, max_n)
    sys.stderr.write("sorting...\n")
    items = name2ID.items()
    items.sort(key=lambda x: x[0])
    fp_out = open(fn_output, "w")
    for key, value in items:
        fp_out.write("%s\t%s\n" % (key, ",".join([str(ID) for ID in value])))
    fp_out.close()
    sys.stderr.write("done\n")

def load_IDs(fn):
    fp = open(fn, "r")
    IDs = []
    for line in fp:
        line = line.strip()
        name, IDstring = line.split("\t")
        IDs.append(IDstring)
    return IDs

if __name__ == "__main__":
    #gnidx = GeonamesIndex("../data/allCountries.txt")
    #print gnidx.get(1122445)
    #create_name2ID_file("../data/allCountries.txt", "test.name2ID")
    IDs = load_IDs("../idx/name2ID.tsv")
    print len(IDs)
