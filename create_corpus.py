import json
import argparse

from gensim.corpora import Dictionary, MmCorpus

from tweet_utils import load_tweets, wakati_tweets


def parse_arg():
    args = argparse.ArgumentParser(description="create corpus from twitter texts in JSON format.")
    args.add_argument("-d", "--output_dictionary", type=str,
                      help="speficy output filename which dictionary will be saved to.")
    args.add_argument("-c", "--output_corpus", type=str,
                      help="speficy output filename which corpus will be saved to.")
    args.add_argument("-u", "--upper_limit", type=float,
                      help="exclude words from dictionary which are appeared over given ratio of documents.")
    args.add_argument("-l", "--lower_limit", type=int,
                      help="exclude words from dictionary which are appeared less than given number of documents.")
    args.add_argument("FILES", type=str, nargs='+', help="specify files.")
    return args.parse_args()


def make_dict_and_corpus(tweets, upper_limit, lower_limit):
    twitter_wakati_texts = wakati_tweets(tweets)
    dictionary = Dictionary(twitter_wakati_texts)
    if upper_limit is not None and lower_limit is not None:
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
