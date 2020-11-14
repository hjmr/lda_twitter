import json
import argparse
import time

from TwitterAPI import TwitterAPI
import config
import tweet_utils


API = 'statuses/user_timeline'
api = TwitterAPI(config.API_KEY, config.API_SECRET_KEY, config.ACCESS_TOKEN, config.ACCESS_TOKEN_SECRET)


def parse_arg():
    args = argparse.ArgumentParser(description="get user timeline.")
    args.add_argument("-f", "--filename", type=str, help="specify output JSON filename.")
    args.add_argument("-u", "--user_id", type=int, help="specify user by user_id.")
    args.add_argument("-s", "--screen_name", type=str, help="specify user by screen_name.")
    args.add_argument("-n", "--num_tweets", type=int, default=200, help="the number of tweets to be obtain.")
    return args.parse_args()


def get_timeline(user_id=None, screen_name=None, count=200):
    tweets = []
    params = {}
    if user_id is not None:
        params['user_id'] = user_id
    elif screen_name is not None:
        params['screen_name'] = screen_name
    else:
        print("One of user_id or screen_name must be specified.")
        return tweets

    min_tweet_id = -1
    while 0 < count:
        c = 200 if 200 < count else count
        count = count - c
        params['count'] = str(c)

        if 0 <= min_tweet_id:
            params['max_id'] = min_tweet_id - 1  # min_twidよりも古いIDのツイートのみを取得する
        res = api.request(API, params=params)
        if res.status_code == 429:  # 時間内の取得数リミットに引っかかった場合
            secs_to_wait = int(res.headers['X-Rate-Limit-Reset'])
            print("Exceed rate limit.")
            print("Waiting for rete limit reset: {} secs.".format(secs_to_wait))
            time.sleep(secs_to_wait)
            continue
        elif res.status_code != 200:  # その他の理由で正常通信出来なかった場合
            print("Failed: %d" % res.status_code)
            break
        elif len(res.json()) == 0:  # 取ってくるツイートがなくなったとき
            print("Seems got all tweets.")
            break

        if 'X-Rate-Limit-Remaining' in res.headers:
            print('Possible API calls: {}'.format(res.headers['X-Rate-Limit-Remaining']))

        for tweet in res:
            tweet_id = int(tweet['id'])
            if min_tweet_id < 0 or tweet_id < min_tweet_id:
                min_tweet_id = tweet_id
                tweets.append(tweet)
        print("min_tweet_id:{}".format(min_tweet_id))
    return tweets


if __name__ == '__main__':
    args = parse_arg()
    tweets = get_timeline(args.user_id, args.screen_name, args.num_tweets)
    if args.filename:
        with open(args.filename, "w+") as f:
            json.dump(tweets, f, indent=2, ensure_ascii=False)
    else:
        tweet_utils.show_tweets(tweets)
