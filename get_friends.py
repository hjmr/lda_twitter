import json
import argparse
import time

from TwitterAPI import TwitterAPI
import config
import utils


API = 'friends/ids'
api = TwitterAPI(config.API_KEY, config.API_SECRET_KEY, config.ACCESS_TOKEN, config.ACCESS_TOKEN_SECRET)


def parse_arg():
    args = argparse.ArgumentParser(description="collect user IDs that the specified user follows.")
    args.add_argument("-f", "--filename", type=str, help="specify output JSON filename.")
    args.add_argument("-u", "--user_id", type=int, help="specify user by user_id.")
    args.add_argument("-s", "--screen_name", type=str, help="specify user by screen_name.")
    args.add_argument("-c", "--count", type=int, default=5000, help="the number of IDs attempt retrieval of.")
    return args.parse_args()


def get_friends(user_id=None, screen_name=None, count=1000):
    friend_ids = []
    params = {}
    if user_id is not None:
        params['user_id'] = user_id
    elif screen_name is not None:
        params['screen_name'] = screen_name
    else:
        print("One of user_id or screen_name must be specified.")
        return friend_ids

    cursor = -1
    while 0 < count:
        c = 5000 if 5000 < count else count
        count = count - c
        params['count'] = c

        if 0 <= cursor:
            params['cursor'] = cursor
        res = api.request(API, params=params)
        rj = res.json()
        if res.status_code == 429:  # 時間内の取得数リミットに引っかかった場合
            secs_to_wait = int(res.headers['X-Rate-Limit-Reset'])
            print("Exceed rate limit.")
            print("Waiting for rete limit reset: {} secs.".format(secs_to_wait))
            time.sleep(secs_to_wait)
            continue
        elif res.status_code != 200:
            print("Error with code: {}".format(res.status_code))
            break
        elif len(rj) == 0:  # とってくるIDがなくなった
            print("Seems got all IDs.")
            break

        if 'X-Rate-Limit-Remaining' in res.headers:
            print('Possible API calls: {}'.format(res.headers['X-Rate-Limit-Remaining']))

        if 'next-cursor' in rj:
            cursor = rj['next-cursor']

        if 'ids' in rj:
            for v in rj['ids']:
                friend_ids.append(v)
    return friend_ids


if __name__ == '__main__':
    args = parse_arg()
    friend_ids = get_friends(args.user_id, args.screen_name, args.count)
    if args.filename:
        with open(args.filename, "w+") as f:
            json.dump(friend_ids, f, indent=2, ensure_ascii=False)
    else:
        print(friend_ids)
