import json
import argparse

import MeCab
from gensim.corpora import Dictionary, MmCorpus

import config
from normalize_text import normalize_text
from wakati_tweets import wakati_tweets, load_tweets

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


def make_dict_and_corpus(tweets):
    twitter_wakati_texts = wakati_tweets(tweets)
    dictionary = Dictionary(twitter_wakati_texts)
    corpus = [dictionary.doc2bow(t) for t in twitter_wakati_texts]
    return dictionary, corpus


if __name__ == '__main__':
    args = parse_arg()
    friends_tweets = load_tweets(args.FILES)
    dictionary, corpus = make_dict_and_corpus(friends_tweets)
    if args.output_dictionary is not None:
        dictionary.save_as_text(args.output_dictionary)
    if args.output_corpus is not None:
        MmCorpus.serialize(args.output_corpus, corpus)
