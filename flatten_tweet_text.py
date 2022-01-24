import argparse

from tweet_utils import load_tweets, normalize_text


def parse_arg():
    args = argparse.ArgumentParser(description="flatten tweet texts.")
    args.add_argument("FILE", type=str, nargs=1, help="specify file.")
    return args.parse_args()


if __name__ == "__main__":
    args = parse_arg()
    tweets = load_tweets(args.FILE)
    print("\n".join([normalize_text(t["text"]) for t in tweets[0]]))
