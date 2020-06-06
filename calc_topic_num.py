import json
import argparse

from gensim.corpora import Dictionary, MmCorpus
from gensim.models import LdaModel, CoherenceModel

import matplotlib.pyplot as plt

from utils import load_tweets
from wakati_tweets import wakati_tweets


def parse_arg():
    args = argparse.ArgumentParser(description="estimate optimal number of topics.")
    args.add_argument("--start", type=int, default=2, help="specify the starting number of topics.")
    args.add_argument("--step", type=int, default=3, help="specify step.")
    args.add_argument("--limit", type=int, default=20, help="specify limit.")
    args.add_argument("-d", "--dictionary", type=str, nargs=1,
                      help="specify output filename which dictionary will be saved to.")
    args.add_argument("-c", "--corpus", type=str, nargs=1,
                      help="specify output filename which corpus will be saved to.")
    args.add_argument("-s", "--save_fig", type=str,
                      help="specify file which the plot will be saved to.")
    args.add_argument("FILES", type=str, nargs='+', help="specify tweets files.")
    return args.parse_args()


def compute_coherence_values(dictionary, corpus, texts, limit, start=2, step=3):
    coherence_values = []
    model_list = []
    for num_topics in range(start, limit, step):
        model = LdaModel(corpus, num_topics=num_topics)
        model_list.append(model)
        coherencemodel = CoherenceModel(model=model, texts=texts, dictionary=dictionary, coherence='c_v')
        coherence_values.append(coherencemodel.get_coherence())

    return model_list, coherence_values


def plot_coherence_values(coherence_values, limit, start=2, step=3):
    x = range(start, limit, step)
    fig = plt.figure()
    plt.plot(x, coherence_values)
    plt.xlabel("Num Topics")
    plt.ylabel("Coherence score")
    plt.legend(("coherence_values"), loc='best')
    return fig


if __name__ == '__main__':
    args = parse_arg()
    texts = wakati_tweets(load_tweets(args.FILES))
    dictionary = Dictionary.load_from_text(args.dictionary[0])
    corpus = MmCorpus(args.corpus[0])
    model_list, coherence_values = compute_coherence_values(
        dictionary, corpus, texts, args.limit, args.start, args.step)

    fig = plot_coherence_values(coherence_values, args.limit, args.start, args.step)
    if args.save_fig is not None:
        fig.savefig(args.save_fig)
    else:
        fig.show()
        input("Press Enter")
