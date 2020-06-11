import json
import argparse

import MeCab
from gensim.corpora import Dictionary, MmCorpus

import config
from normalize_text import normalize_text
from utils import load_tweets
from wakati_tweets import wakati_tweets

POS_USED = ['名詞', '動詞', '副詞', '形容詞', '形容動詞', '感動詞']
tagger = MeCab.Tagger("-d {}".format(config.MECAB_DIC))


def parse_arg():
    args = argparse.ArgumentParser(description="create corpus from twitter texts in JSON format.")
    args.add_argument("-d", "--output_dictionary", type=str,
                      help="speficy output filename which dictionary will be saved to.")
    args.add_argument("-c", "--output_corpus", type=str,
                      help="speficy output filename which corpus will be saved to.")
    args.add_argument("-u", "--upper_limit", type=float, default=0.5,
                      help="exclude words from dictionary which are appeared over given ratio of documents.")
    args.add_argument("-l", "--lower_limit", type=int, default=5,
                      help="exclude words from dictionary which are appeared less than given number.")
    args.add_argument("FILES", type=str, nargs='+', help="specify files.")
    return args.parse_args()


def make_dict_and_corpus(tweets, upper_limit, lower_limit):
    twitter_wakati_texts = wakati_tweets(tweets)
    dictionary = Dictionary(twitter_wakati_texts)
    dictionary.filter_extremes(no_below=lower_limit, no_above=upper_limit)
    corpus = [dictionary.doc2bow(t) for t in twitter_wakati_texts]
    return dictionary, corpus


if __name__ == '__main__':
    args = parse_arg()
    friends_tweets = load_tweets(args.FILES)
    dictionary, corpus = make_dict_and_corpus(friends_tweets, args.upper_limit, args.lower_limit)
    if args.output_dictionary is not None:
        dictionary.save_as_text(args.output_dictionary)
    if args.output_corpus is not None:
        MmCorpus.serialize(args.output_corpus, corpus)
