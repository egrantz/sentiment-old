from TwitterAPI import TwitterAPI #https://github.com/geduldig/TwitterAPI
import json

# Your access information goes here
CONSUMER_KEY = "<your key here>"
CONSUMER_SECRET = "<your secret here>"
ACCESS_TOKEN_KEY = "<your key here>"
ACCESS_TOKEN_SECRET = "<your secret here>"

api = TwitterAPI(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN_KEY, ACCESS_TOKEN_SECRET)

SEARCH_TERM = "dog"

## "raw" stream
r = api.request('statuses/sample')

## stream filtering by search term
#r = api.request('statuses/filter', {'track': SEARCH_TERM})

## search by search term
#r = api.request('search/tweets', {'q': SEARCH_TERM, 'count':100})

for item in r:
  if 'text' in item:
    print(json.dumps(item))
    #print(json.dumps(item).encode('utf8')) #replace above line with this for windows

