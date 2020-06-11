import json
import argparse

from gensim.corpora import Dictionary, MmCorpus
from gensim.models import LdaModel


def parse_arg():
    args = argparse.ArgumentParser(description="create a LDA model.")
    args.add_argument("-d", "--dictionary", type=str, nargs=1,
                      help="specify dictionary to be loaded.")
    args.add_argument("-c", "--corpus", type=str, nargs=1,
                      help="specify corpus to be loaded.")
    args.add_argument("-n", "--num_topics", type=int, default=10,
                      help="specify the number of topics.")
    args.add_argument("-u", "--upper_limit", type=float, default=0.5,
                      help="exclude words from dictionary which are appeared over given ratio of documents.")
    args.add_argument("-l", "--lower_limit", type=int, default=5,
                      help="exclude words from dictionary which are appeared less than given number.")
    args.add_argument("-o", "--output_file", type=str, nargs=1,
                      help="specify filename which the LDA model will be saved to.")
    return args.parse_args()


if __name__ == "__main__":
    args = parse_arg()
    corpus = MmCorpus(args.corpus[0])
    dictionary = Dictionary.load_from_text(args.dictionary[0])
    dictionary.filter_extremes(no_below=args.lower_limit, no_above=args.upper_limit)
    model = LdaModel(corpus=corpus, id2word=dictionary, num_topics=args.num_topics)
    model.save(args.output_file[0])
