import re
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


def check_if_not_use(word, feature):
    yn = False
    POS_NOT_USED = [("名詞", "数")]
    STOP_WORDS = []
    if word in STOP_WORDS:
        yn = True
    else:
        for p in POS_NOT_USED:
            if len(p) == 1:
                yn = (p[0] == feature[0])
            else:
                yn = (p[0] == feature[0] and p[1] == feature[1])
    return yn


def check_if_use(word, feature):
    yn = False
    POS_USED = [("名詞"), ("形容詞", "自立")]
    for p in POS_USED:
        if len(p) == 1:
            yn = (p[0] == feature[0])
        else:
            yn = (p[0] == feature[0] and p[1] == feature[1])
    return yn


def remove_urls(text):
    text = re.sub("https?://[\w!\?/\+\-_~=;\.,\*&@#\$%\(\)'\[\]]+", "", text)
    return text


def remove_screen_names(text):
    text = re.sub("@[A-Za-z0-9_]+", "", text)
    return text


def wakati_text(text):
    wakati = []
    tagger.parse('')
    n = tagger.parseToNode(normalize_text(text))
    while n:
        f = n.feature.split(',')
        if check_if_use(n.surface, f) == True and check_if_not_use(n.surface, f) != True:
            w = f[6] if f[6] != '*' else n.surface
            if 1 < len(w):
                wakati.append(w)
        n = n.next
    return wakati


def wakati_texts(texts):
    wakati_texts = [wakati_text(remove_screen_names(remove_urls(t))) for t in texts]
    return wakati_texts


def wakati_tweets(tweets):
    twitter_wakati_texts = wakati_texts([t['text'] for t in tweets])
    return twitter_wakati_texts


if __name__ == "__main__":
    args = parse_arg()
    tweets = utils.load_tweets(args.FILES)
    texts = wakati_tweets(tweets)
    print(texts[0])
