import json
import argparse

import MeCab

import config
from normalize_text import normalize_text

POS_USED = ['名詞', '動詞', '副詞', '形容詞', '形容動詞', '感動詞']
tagger = MeCab.Tagger("-d {}".format(config.MECAB_DIC))


def parse_arg():
    args = argparse.ArgumentParser(description="make wakati texts from tweets.")
    args.add_argument("FILES", type=str, nargs='+', help="specify files.")
    return args.parse_args()


def load_tweets(files):
    tweets = []
    for fn in files:
        with open(fn, "r") as f:
            tweets.append(json.load(f))
    return tweets


def check_stop_words(feature):
    yn = False
    if feature[1] == '数':
        yn = True
    elif feature[1] == '固有名詞' and feature[2] == '一般':
        yn = True
    return yn


def wakati_line(line):
    wakati = []
    tagger.parse('')
    n = tagger.parseToNode(normalize_text(line))
    while n:
        f = n.feature.split(',')
        if f[0] in POS_USED and check_stop_words(f) != True:
            wakati.append(f[6]) if f[6] != '*' else wakati.append(n.surface)
        n = n.next
    return wakati


def wakati_texts(texts):
    wakati_texts = [wakati_line(t) for t in texts]
    return wakati_texts


def wakati_tweets(tweets):
    twitter_wakati_texts = wakati_texts([t['text'] for t in tweets])
    return twitter_wakati_texts


if __name__ == "__main__":
    args = parse_arg()
    tweets = load_tweets(args.FILES)
    texts = wakati_tweets(tweets)
    print(texts[0])
