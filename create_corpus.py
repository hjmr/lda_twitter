import json
import argparse

import MeCab
from gensim.corpora import Dictionary, MmCorpus

import config
from normalize_text import normalize_text

POS_USED = ['名詞', '動詞', '副詞', '形容詞', '形容動詞', '感動詞']
tagger = MeCab.Tagger("-d {}".format(config.MECAB_DIC))


def parse_arg():
    args = argparse.ArgumentParser(description="create corpus from twitter texts in JSON format.")
    args.add_argument("-d", "--output_dictionary", type=str,
                      help="speficy output filename which dictionary will be saved to.")
    args.add_argument("-c", "--output_corpus", type=str,
                      help="speficy output filename which corpus will be saved to.")
    args.add_argument("FILES", type=str, nargs='+', help="specify files.")
    return args.parse_args()


def load_twitter_data(files):
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


def make_dict_and_corpus(tweets):
    twitter_wakati_texts = [wakati_line(t['text']) for t in tweets]
    dictionary = Dictionary(twitter_wakati_texts)
    corpus = [dictionary.doc2bow(t) for t in twitter_wakati_texts]
    return dictionary, corpus


if __name__ == '__main__':
    args = parse_arg()
    friends_tweets = load_twitter_data(args.FILES)
    dictionary, corpus = make_dict_and_corpus(friends_tweets)
    if args.output_dictionary is not None:
        dictionary.save_as_text(args.output_dictionary)
    if args.output_corpus is not None:
        MmCorpus.serialize(args.output_corpus, corpus)
