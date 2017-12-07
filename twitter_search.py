"""Query Twitter API and retrieve relevant tweets.

Takes a search query and various other possible parameters, outputs relevant
tweets to a .bz2 file.

Note: Twitter API requires a user access token, secret, consumer key and
consumer secret. See tutorial located here for how to generate credentials:
https://www.slickremix.com/docs/how-to-get-api-keys-and-tokens-for-twitter/

These should be saved in this order, on separate lines, in a file named
"twitter_credentials.txt" in the project root directory.

Keep your credentials secret and do not push to remote repo! .gitignore should
automatically stop this from happening.

Script inspired by tutorial at:
http://socialmedia-class.org/twittertutorial.html
"""

import re        # for checking whether file name extension included
import os        # for checking whether credentials.txt file present
import bz2       # for writing to .bz2 file
import io        # for wrapping string output to encode
import json      # for converting Twitter library object to dictionary
import sys       # to determine if invoked from command line or IDE
import argparse
from test.twitter_search import validate_kwargs
from twitter import Twitter, OAuth


def twitter_OAuth():
    """Create an OAuth link to Twitter API"""
    # Read in credentials for OAuth
    if 'twitter_credentials.txt' in os.listdir():
        creds = open('twitter_credentials.txt', 'r')
        access_token = creds.readline().strip()
        access_secret = creds.readline().strip()
        consumer_key = creds.readline().strip()
        consumer_secret = creds.readline().strip()
        creds.close()
    else:
        access_token = input("Please enter access token:\n")
        access_secret = input("Please enter access token secret:\n")
        consumer_key = input("Please enter consumer key:\n")
        consumer_secret = input("Please enter consumer key secret:\n")

    # Initiate the connection to Twitter Streaming API
    oauth = OAuth(access_token, access_secret, consumer_key, consumer_secret)
    return Twitter(auth=oauth)


def search_tweets(query, **kwargs):
    """Retrieve tweets according to provided parameters and export to bz2 file.

    Arguments:
        query (str): The search query.
        kwargs (dict): Optional arguments to refine search:
        - count (int): Number of tweets to retrieve. Max 100, default 15.
        - file (str): Filename to write to. Defaults to "tweets.txt.bz2".
        - lang (str): A valid ISO 639-1 code, e.g. 'en'.
        - result_type (str): Either 'recent', 'popular' or 'mixed' (default).
        - exact (bool): only include exact phrase matches
        - until (str): restrict to tweets up til YYYY-MM-DD (e.g. '2017-11-20')
        - since_id (int): min ID value for returned tweets
        - max_id (int): max ID value for returned tweets
        - include_entities (str): include entities node? (default = false)

    Returns:
        None
    """
    # Validate kwargs
    validate_kwargs(**kwargs)

    # If count specified extract that, otherwise default to 15
    extra_to_retrieve = 15
    if 'count' in kwargs:
        extra_to_retrieve = kwargs.pop('count')

    # Extract file name to write results to. Add '.txt.bz2' extention if needed
    filename = './tweets/tweets.txt.bz2'
    if 'file' in kwargs:
        filename = './tweets/' + kwargs.pop('file')
        if not re.search(r'.txt.bz2$', filename):
            filename = filename + '.txt.bz2'

        # If exact search specified, enclose in quotation marks (multi-word queries)
    if 'exact' in kwargs:
        exact = kwargs.pop('exact')
        if len(query) > 1 and exact:
            query = '"' + query + '"'

    twitter = twitter_OAuth()

    # Save tweets to .bz2 file
    output = bz2.BZ2File(filename, 'w')
    tweets_parsed = 0
    max_id = float('inf')
    print('Retrieving tweets for query {}...'.format(query))

    # BZ2 needs strings to be encoded, so use TextWrapper
    with io.TextIOWrapper(output, encoding='utf-8') as wrapper:
        # If retrieving > 100 tweets, will need several API calls
        while extra_to_retrieve > 0:
            if tweets_parsed > 0:
                print('Total tweets parsed: {}'.format(tweets_parsed))
            to_retrieve = min(extra_to_retrieve, 100)   # API only gives 100 max
            tweets_parsed_last_round = tweets_parsed

            # Retrieve tweets by calling the Twitter search API
            tweets = twitter.search.tweets(q=query, count=to_retrieve, **kwargs)

            # Convert each tweet JSON object to a dictionary and write to file
            for tweet in tweets['statuses']:
                wrapper.write(json.dumps(tweet))
                wrapper.write('\n')
                # Keep track of oldest tweet. Will use as threshold for next batch
                if tweet['id'] < max_id:
                    max_id = tweet['id']
                    kwargs['max_id'] = max_id
                extra_to_retrieve -= 1
                tweets_parsed += 1

            # If no new tweets retrieved, break loop
            if tweets_parsed == tweets_parsed_last_round:
                extra_to_retrieve = 0
            kwargs['max_id'] -= 1    # decrement to avoid including threshold tweet twice

    output.close()

    # Check API rate limit status
    lim = twitter.application.rate_limit_status()['resources']['search']['/search/tweets']
    print('\nRetrieved {} relevant tweets'.format(tweets_parsed))
    print('Saved to file {}'.format(filename))
    print('\nRemaining API calls for current time period: {} of {}'.format(lim['remaining'], lim['limit']))


# Invoke function if called from console. Note I don't actually understand this
if sys.stdout.isatty():
    parser = argparse.ArgumentParser(description='Scrape tweets for a given query.')
    parser.add_argument('query', help='The search query', type=str, default='happy')
    parser.add_argument('-l', '--lang', help='Restrict retrieved tweets to a given language', type=str)
    parser.add_argument('-r', '--result_type', help='Choose between recent and popular tweets', type=str,
                        choices=['recent', 'popular', 'mixed'])
    parser.add_argument('-c', '--count', help='Number of tweets to retrieve', type=int)
    parser.add_argument('-u', '--until', help='Final date to retrieve tweets until', type=str, metavar='YYYY-MM-DD')
    parser.add_argument('-s', '--since_id', help='Min tweet ID to retrieve', type=int)
    parser.add_argument('-m', '--max_id', help='Max tweet ID to retrieve', type=int)
    parser.add_argument('-i', '--include_entities', help='Whether to include entities node', type=str,
                        choices=['true', 'false'])
    parser.add_argument('-f', '--file', help='File name to write the results to.', type=str)
    parser.add_argument('-e', '--exact', help='Only retrieve exact query matches', action='store_true')

    args = parser.parse_args()
    dict_args = vars(args)

    # Convert args to a dictionary
    args = {}
    q = dict_args.pop('query')

    for key, value in dict_args.items():
        if value:
            args[key] = value

    search_tweets(q, **args)
