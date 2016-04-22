# Your functions go here!













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
