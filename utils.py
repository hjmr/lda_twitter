import json
import argparse

import MeCab

import config
from normalize_text import normalize_text

tagger = MeCab.Tagger("-d {}".format(config.MECAB_DIC))


def parse_arg():
    args = argparse.ArgumentParser(description="make wakati texts from tweets.")
    args.add_argument("FILES", type=str, nargs='+', help="specify files.")
    return args.parse_args()


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


def check_stop_words(word, feature):
    yn = False
    POS_USED = ["名詞", "形容詞"]
    STOP_WORDS = []

    if feature[0] not in POS_USED:
        yn = True
    elif feature[1] == '数':
        yn = True
    elif word in STOP_WORDS:
        yn = True
    return yn


def wakati_text(text):
    wakati = []
    tagger.parse('')
    n = tagger.parseToNode(normalize_text(text))
    while n:
        f = n.feature.split(',')
        if check_stop_words(n.surface, f) != True:
            w = f[6] if f[6] != '*' else n.surface
            if 1 < len(w):
                wakati.append(w)
        n = n.next
    return wakati


def wakati_texts(texts):
    wakati_texts = [wakati_text(t) for t in texts]
    return wakati_texts


def wakati_tweets(tweets):
    twitter_wakati_texts = wakati_texts([t['text'] for t in tweets])
    return twitter_wakati_texts


if __name__ == "__main__":
    args = parse_arg()
    tweets = utils.load_tweets(args.FILES)
    texts = wakati_tweets(tweets)
    print(texts[0])
