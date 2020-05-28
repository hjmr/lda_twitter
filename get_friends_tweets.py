import json
import argparse
import time

from TwitterAPI import TwitterAPI
import config
import utils
from get_friends import get_friends
from get_timeline import get_timeline
from get_userinfo import get_userinfo


SHOW_USER = 'users/show'
api = TwitterAPI(config.API_KEY, config.API_SECRET_KEY, config.ACCESS_TOKEN, config.ACCESS_TOKEN_SECRET)


def parse_arg():
    args = argparse.ArgumentParser(description="get user's friends' timelines.")
    args.add_argument("-f", "--base_filename", type=str,
                      help="specify base filename of output. the actual filename will be <base_filename>_user_id.")
    args.add_argument("-u", "--user_id", type=int, help="specify user by user_id.")
    args.add_argument("-s", "--screen_name", type=str, help="specify user by screen_name.")
    args.add_argument("-n", "--num_tweets", type=int, default=200, help="the number of tweets to be obtain.")
    args.add_argument("-c", "--count", type=int, default=5000, help="the number of friends attempt retrieval of.")
    return args.parse_args()


def get_friends_tweets(user_id=None, screen_name=None, num_friends=1000, num_tweets=200):
    tweets = []
    friend_ids = get_friends(user_id, screen_name, num_friends)
    for fid in friend_ids:
        user_tweets = {}
        user_info = get_userinfo(fid, None)
        user_tweets['user_id'] = userinfo['id']
        user_tweets['screen_name'] = userinfo['screen_name']
        user_timeline = get_timeline(fid, None, num_tweets)
        user_tweets['text'] = ' '.join([t['text'] for t in user_timeline])
        tweets.append(user_tweets)
    return tweets


if __name__ == '__main__':
    args = parse_arg()
    friends_tweets = get_friends_tweets(args.user_id, args.screen_name, args.count, args.num_tweets)
    if args.base_filename is not None:
        for t in friends_tweets:
            user_id = t['user_id']
            with open("{}_{}".format(args.base_filename, user_id)) as f:
                json.dump(t, f, indent=2, ensure_ascii=False)
    else:
        for t in friends_tweets:
            screen_name = t['screen_name']
            text = t['text']
            print("{}: {}".format(screen_name, text[:10]))
