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
sys.path.append("./src")
import BaseHTTPServer
import cgi
from urlparse import urlparse, parse_qs
import json
from gn_tagger import GNTagger

_HTML_FN = "gnt.html"

class GNTHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    gnt = None

    def _process_parse(self, params):
        self.send_response(200)
        self.send_header("Content-type", "text/json")
        self.end_headers()
        resp = None
        if "text" not in params:
            resp = json.dumps({"success": 0, "msg": "no 'text' parameters provided!"})
        else:
            bound_chars = None
            if "bound_chars" in params:
                bound_chars = params["bound_chars"][0]
                if bound_chars == "":
                    bound_chars = None
            text = params["text"][0].lower()
            matches = GNTHandler.gnt.parse(text, bound_chars)
            resp = json.dumps(matches)
        self.wfile.write(resp)

    def do_GET(self):
        print self.path
        if self.path.startswith("/gnt.html"):
            fp = open(_HTML_FN, "r")
            html = fp.read()
            fp.close()
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(html)
        else:
            self._process_parse(self._GET_params())

    def do_POST(self):
        self._process_parse(self._POST_params())
    
    def _POST_params(self):
        ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
        if ctype == 'multipart/form-data':
            postvars = cgi.parse_multipart(self.rfile, pdict)
        elif ctype == 'application/x-www-form-urlencoded':
            length = int(self.headers.getheader('content-length'))
            postvars = cgi.parse_qs(self.rfile.read(length), keep_blank_values=1)
        else:
            postvars = {}
        return postvars

    def _GET_params(self):
        return parse_qs(urlparse(self.path).query)

def usage():
    print """usage:  gnt_start_server GEONAMES_FILE IDX_PATH [HOST [PORT]]
    
    GEONAMES_FILE: path to the 'allCountries.txt' file
    IDX_PATH:      path of the index created with 'gnt_index.py'
    HOST:          hostname of the server (defaults to 'localhost')
    PORT:          port of the server (defaults to 55555) 
"""
    sys.exit(1)

       
if __name__ == "__main__":
    if len(sys.argv) < 3:
        usage()
    fn_in = sys.argv[1]
    idx_path = sys.argv[2].rstrip("/")
    host = "localhost"
    port = 55555
    if len(sys.argv) == 4:
        host = sys.argv[3]
    if len(sys.argv) == 5:
        port = int(sys.argv[4])
    if len(sys.argv) > 5:
        usage()
    print host, port
    print "loading geonames tagger data..."
    gnt = GNTagger(fn_in, idx_path+"/trie.bin", idx_path+"/name2ID.tsv")
    GNTHandler.gnt = gnt
    print "starting server..."
    server_class = BaseHTTPServer.HTTPServer
    httpd = server_class((host, port), GNTHandler)
    try:
        print "listening (Ctr-C to quit)"
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
