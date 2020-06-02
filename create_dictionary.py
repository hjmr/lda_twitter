import json
import argparse
import pickle

import MeCab
from gensim.corpora import Dictionary

import config
from normalize_text import normalize_text

POS_USED = ['名詞', '動詞', '副詞', '形容詞', '形容動詞', '感動詞']
tagger = MeCab.Tagger("-d {}".format(config.MECAB_DIC))


def parse_arg():
    args = argparse.ArgumentParser(description="create corpus from twitter texts in JSON format.")
    args.add_argument("-f", "--files", type=str, nargs='+', help="specify files.")
    args.add_argument("-o", "--output", type=str, help="speficy output filename which corpus will be saved to.")
    return args.parse_args()


def load_twitter_data(files):
    tweets = []
    for fn in files:
        with open(fn, "r") as f:
            tweets.append(json.load(f))
    return tweets


def wakati_line(line):
    wakati = []
    tagger.parse('')
    n = tagger.parseToNode(normalize_text(line))
    while n:
        f = n.feature.split(',')
        if f[0] in POS_USED:
            wakati.append(f[6]) if f[6] != '*' else wakati.append(n.surface)
        n = n.next
    return wakati


def make_dictionary(tweets):
    twitter_wakati_texts = [wakati_line(t['text']) for t in tweets]
    dictionary = Dictionary(twitter_wakati_texts)
    return dictionary


if __name__ == '__main__':
    args = parse_arg()
    friends_tweets = load_twitter_data(args.files)
    dictionary = make_dictionary(friends_tweets)
    if args.output is not None:
        with open(args.output, "wb") as f:
            pickle.dump(dictionary, f)
