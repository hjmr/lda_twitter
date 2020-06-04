import json
import argparse

from gensim.corpora import Dictionary, MmCorpus
from gensim.models import CoherenceModel
from gensim.models.wrappers import LdaMallet

from wakati_tweets import wakati_tweets, load_tweets


def parse_arg():
    args = argparse.ArgumentParser(description="estimate optimal number of topics.")
    args.add_argument("-d", "--dictionary", type=str, nargs=1,
                      help="speficy output filename which dictionary will be saved to.")
    args.add_argument("-c", "--corpus", type=str, nargs=1,
                      help="speficy output filename which corpus will be saved to.")
    args.add_argument("FILES", type=str, nargs='+', help="specify tweets files.")
    return args.parse_args()


def compute_coherence_values(dictionary, corpus, texts, limit, start=2, step=3):
    coherence_values = []
    model_list = []
    for num_topics in range(start, limit, step):
        model = LdaMallet(mallet_path, corpus=corpus, num_topics=num_topics, id2word=id2word)
        model_list.append(model)
        coherencemodel = CoherenceModel(model=model, texts=texts, dictionary=dictionary, coherence='c_v')
        coherence_values.append(coherencemodel.get_coherence())

    return model_list, coherence_values


if __name__ == '__main__':
    args = parse_arg()
    tweets = load_tweets(args.FILES)
    dictionary = Dictionary.load_from_text(args.dictionary)
    corpus = MmCorpus(args.corpus)
