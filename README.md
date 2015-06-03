# geonames tagger #
Allows to tag all occurences of geonames places in a given text.

## Usage ##
Go to the `geonames_tagger` directory.

### Create index ###
Needs ~1 hour on MacBook Pro and 4.9GB of RAM:
```
$ python gnt_index.py data/allCountries.txt idx001
```
### Start server ###
Start the http server:
```
$ python gnt_server.py -h "localhost" -p 55555 idx001
```
### Requests ###
Make request via python script. The must always be utf-8 encoded:
```
$ python gnt_request -h "localhost" -p 55555 txtfile
```
Or, make http request (returns json result):
```
http://localhost:55555/service
POST parameter: text=<utf-8 encoded text>
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
