# geonames tagger #
Tags all substrings (or tokens) existing as place names in the geonames gazetteer in O(len(text)) time.

## Usage ##
Download the `allCountries.zip` file from the geonames Web site and
extract the `allCountries.txt` file (e.g., into the `geonames_tagger/data` folder). 

### Create index ###
Needs ~1 hour on MacBook Pro and 4.9GB of RAM:
```
$ python gnt_index.py data/allCountries.txt idx001
```
### Start tagging service ###
Start the http server:
```
$ python gnt_server.py -h "localhost" -p 55555 idx001
```
### Requests ###
Make tagging POST request via a python script (check source of `gnt_request.py`). The submitted text must always be utf-8 encoded:
```
$ python gnt_request -h "localhost" -p 55555 txtfile
```
Or, make http POST request directly (returns the result as json):
```
http://localhost:55555/service
POST parameter: text=<utf-8 encoded text>
```
Using curl (POST):
```
$ curl --data "text=the text to parse" http://localhost:55555
```
Using curl (GET):
```
$ curl http://localhost:55555?text=aplacename
```
The resulting json looks like:
```
{ 
  "success":   1,
  "n_matches": N, 
  "matches":   [
                 {
                   "token":  TOKEN,
                   "idx":    [START,END],
                   "gnrecs": [ 
                               [COLS OF REC IN allCountries.txt FILE],
                               ... 
                             ]
                 },
                 ...
               ]
}
```
In case of an error:
```
{ 
  "success": 0,
  "msg":     MESSAGE
}
```
