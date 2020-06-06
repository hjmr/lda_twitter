import json


def show_tweets(tweets):
    for t in tweets:
        print("------------------------------------")
        print("tweet id: {}".format(t['id']))
        print("screen_name: {}".format(t['user']['screen_name']))
        print("user id: {}".format(t['user']['id']))
        print(t['text'])


def load_tweets(files):
    tweets = []
    for fn in files:
        with open(fn, "r") as f:
            tweets.append(json.load(f))
    return tweets
