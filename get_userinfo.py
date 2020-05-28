import argparse

from TwitterAPI import TwitterAPI
import config


API = 'users/show'
api = TwitterAPI(config.API_KEY, config.API_SECRET_KEY, config.ACCESS_TOKEN, config.ACCESS_TOKEN_SECRET)


def parse_arg():
    args = argparse.ArgumentParser(description="show user info.")
    args.add_argument("-u", "--user_id", type=int, help="specify user by user_id.")
    args.add_argument("-s", "--screen_name", type=str, help="specify user by screen_name.")
    return args.parse_args()


def get_userinfo(user_id=None, screen_name=None):
    params = {}
    if user_id is not None:
        params['user_id'] = user_id
    elif screen_name is not None:
        params['screen_name'] = screen_name
    else:
        print("One of user_id or screen_name must be specified.")
        return None

    res = api.request(API, params=params)
    if res.status_code != 200:
        print("Error with code: {}".format(res.status_code))

    return res.json()


if __name__ == '__main__':
    args = parse_arg()
    user_info = get_userinfo(args.user_id, args.screen_name)
    print("user_id: {}".format(user_info['id']))
    print("screen_name: {}".format(user_info['screen_name']))
