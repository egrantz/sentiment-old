# Your functions go here!
#part 1a
import re #import regex
listy = [] #create an empty list
def extract_words(words):
  words = re.split("[^\w']+", words)
  for word in words:
    if word != '':
      listy.append(word) #adds words that are not punctuation, empty space, to list
  return listy #returns a list of all words, stripped of the punctuation between letters and empty spces between letters

#part 1b
def load_sentiments(file): #created a function with parameter: file
  dictsentiment = {} #created an empty dictionary
  openfile = open(file) #open the file typed in on the command line level, assign it to variable openfile
  for row in openfile:
    row = row.strip().split(',') #.strip removes leading and trailing white space, .split splits the row at the comma, turns row into a tuple consisting of: the part before the comma, the comma, and the part after the comma
    dictsentiment[row[0]] = row[1] #inserts results of this for loop, into the previously empty dictionary
  return dictsentiment #returns the dictionary, now not empty

#part 1c
#creating a function that takes in a text to analyze, and a dictionary to analyze it with, as parameters
def text_sentiment(texty, dictionarrio):
  #the sentiment value should default to 0, if it is not in the dictionary, thus set default value to 0
  sentiment_val = 0
  #create a variable that takes the value of the text string, that has been run through the extract_words fn
  words = extract_words(texty)
  for word in words:
    #if loop, that takes sentiment value of words in dictionary and adds them together for the whole string
    if word in dictionarrio:
      sentiment_val = sentiment_val + int(dictionarrio[word])
  return sentiment_val #returns sentiment value of whole string 

#part 2a
import json
#create load_tweets function, taking the parameter of file
def load_tweets(file):
  #create variable, fill it with value of the file input on the command line
  tweets = open(file) 
  #creating an empty list for future tweets to be put in
  tweetslist = list()
  #for each line in the opened file
  for line in tweets:
    #loads each line from the tweets file, and parses it using json
    dictionary = json.loads(line)
    #turns the above variable into a dictionary
    dictionary = {dictionary}
    #creates a variable that pulls the data within the dictionary, associated with the key "created_at"
    created_at = data["created_at"] 
    #creates a variable called dictionary, that is a dictionary, pulling the below fields from the tweets file
    dictionary = {
      "created_at": dictionary.get("created_at"), 
      "user.screen_name": dictionary.get("user.screen_name"),
      "text": dictionary.get("text"), 
      "entities.hashtags[i].text": dictionary.get("entities.hashtags[i].text"),
      "retweet_count": dictionary.get("retweet_count"),
      "favorite_count": dictionary.get("favorite_count")
      }
    #adds dictionary of tweets, to inside the tweetslist
    tweetslist.append(dictionary)
  #returns list, with dictionary inside
  return tweetslist


####################################
## DO NOT EDIT BELOW THIS POINT!! ##
## #################################

# Run the method specified by the command-line
if __name__ == '__main__':
  #for parsing and friendly command-line error messages
  import argparse 
  parser = argparse.ArgumentParser(description="Analyze Tweets")
  subparsers = parser.add_subparsers(description="commands", dest='cmd')
  subparsers.add_parser('load_tweets', help="load tweets from file").add_argument('filename')
  subparsers.add_parser('popularity', help="show average popularity of tweet file").add_argument('filename')
  subparsers.add_parser('extract_words', help="show list of words from text").add_argument(dest='text', nargs='+')
  subparsers.add_parser('load_sentiments', help="load word sentiment file").add_argument('filename')

  sentiment_parser = subparsers.add_parser('sentiment', help="show sentiment of data. Must include either -f (file) or -t (text) flags.")
  sentiment_parser.add_argument('-f', help="tweets file to analyze", dest='tweets')
  sentiment_parser.add_argument('-t', help="text to analyze", dest='text', nargs='+')
  sentiment_parser.add_argument('-s', help="sentiment file", dest="sentiments", required=True)

  subparsers.add_parser('hashtag_counts', help="show frequency of hashtags in tweet file").add_argument('filename')

  hashtag_parser = subparsers.add_parser('hashtag', help="show sentiment of hashtags.")
  hashtag_parser.add_argument('-f', help="tweets file to analyze", dest='tweets', required=True)
  hashtag_parser.add_argument('-s', help="sentiment file", dest="sentiments", required=True)
  hashtag_parser.add_argument('-q', help="hashtag to analyze", dest="query", default=None)

  correlation_parser = subparsers.add_parser('correlation', help="show correlation between popularity and sentiment of tweets")  
  correlation_parser.add_argument('-f', help="tweets file to analyze", dest='tweets', required=True)
  correlation_parser.add_argument('-s', help="sentiment file", dest="sentiments", required=True)

  args = parser.parse_args()

  try:
    if args.text:
      args.text = ' '.join(args.text) #combine text args
  except:
    pass

  #print(args) #for debugging

  # call function based on command given
  if args.cmd == 'load_tweets':
    tweets = load_tweets(args.filename)
    for tweet in tweets:
      print(tweet)

  elif args.cmd == 'popularity':
    print(popularity(args.filename))

  elif args.cmd == 'hashtag_counts':
    for key,value in hashtag_counts(args.filename):
      print(str(key),":",value)

  elif args.cmd == 'extract_words':
    print(extract_words(args.text))

  elif args.cmd == 'load_sentiments':
    for key,value in sorted(load_sentiments(args.filename).items()):
      print(key,value)

  elif args.cmd == 'sentiment':
    if args.tweets == None: #no file, do text
      sentiment = text_sentiment(args.text, load_sentiments(args.sentiments))
      print('"'+args.text+'":', sentiment)
    elif args.text == None: #no text, do file
      rated_tweets = tweet_sentiments(args.tweets, args.sentiments)
      for tweet in rated_tweets:
        print(tweet)
    else:
      print("Must include -f (tweet filename) or -t (text) flags to calculate sentiment.")

  elif args.cmd == 'hashtag':
    if(args.query == None): #split to test optional param
      rated_tags = hashtag_sentiments(args.tweets, args.sentiments)
    else:
      rated_tags = hashtag_sentiments(args.tweets, args.sentiments, args.query)
    for key,value in rated_tags:
      print(str(key),":",value)

  elif args.cmd == 'correlation':
    print("Correlation between popularity and sentiment: r="+str(popular_sentiment(args.tweets, args.sentiments)))