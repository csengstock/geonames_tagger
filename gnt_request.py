#!/usr/bin/python

import sys
import json
import urllib
import urllib2

def send_post(host, port, params, path=""):
    url = "http://%s:%d/%s" % (host, port, path)
    data = urllib.urlencode(params)
    req = urllib2.Request(url, data)
    response = urllib2.urlopen(req)
    return response.read()

def usage():
    print """Usage:  gnt_request TEXT_FILE [host [port]]

    TEXT_FILE: text to parse. Use '-' to read from stdin.
    HOST:      hostname of server (defaults to 'localhost')
    PORT:      port of server (defaults to 55555)
"""
    sys.exit(1)

if __name__ == "__main__":
    host = "localhost"
    port = 55555
    if len(sys.argv) < 2:
        usage()
    fn = sys.argv[1]
    fp = None
    if fn == "-":
        print "reading from stdin. Use Ctrl-D (linux) or Ctrl-O > Ctrl-D (osx) for EOF"
        fp = sys.stdin
    else:
        fp = open(fn, "r")
    if len(sys.argv) == 3:
        host = sys.argv[2]
    if len(sys.argv) == 4:
        port = int(sys.argv[3])
    if len(sys.argv) > 4:
        usage()
    txt = fp.read()
    resp = send_post(host, port, {"text": txt})
    resp = json.loads(resp)
    if resp["success"] == 0:
        print resp
    else:
        print "response:", resp["n_matches"], "matches"
        for rec in resp["matches"]:
            print "---"
            print rec
