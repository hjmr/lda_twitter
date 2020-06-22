import json
import argparse

from gensim.corpora import Dictionary, MmCorpus
from gensim.models import LdaModel, CoherenceModel

import numpy as np
import matplotlib.pyplot as plt

from tweet_utils import load_tweets, wakati_tweets


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
    args.add_argument("-m", "--coherence_measure", type=str, default="c_v",
                      help="specify coherence measure to be used.")
    args.add_argument("-r", "--repeat", type=int, default=1,
                      help="the number of times to repeat calculation for more accurate values.")
    args.add_argument("FILES", type=str, nargs='+', help="specify tweets files.")
    return args.parse_args()


def compute_coherence_values(dictionary, corpus, texts, limit, start=2, step=3, coherence_measure="c_v"):
    coherence_values = []
    perplexities = []
    for num_topics in range(start, limit, step):
        model = LdaModel(corpus, num_topics=num_topics)
        perplexities.append(np.exp2(-model.log_perplexity(corpus)))
        coherencemodel = CoherenceModel(model=model, texts=texts, dictionary=dictionary, coherence=coherence_measure)
        coherence_values.append(coherencemodel.get_coherence())

    return np.array(coherence_values, dtype=np.float32), np.array(perplexities, dtype=np.float32)


def plot_coherence_values(coherence_values, perplexities, limit, start=2, step=3):
    x = range(start, limit, step)
    fig = plt.figure()
    ax1 = fig.add_subplot(111)
    ax2 = ax1.twinx()

    ax1.plot(x, coherence_values, "C0", label="Coherence score")
    ax1.set_xlabel("Num Topics")
    ax1.set_ylabel("Coherence score")

    ax2.plot(x, perplexities, "C1", label="Perplexity")
    ax2.set_ylabel("Perprexity")

    h1, l1 = ax1.get_legend_handles_labels()
    h2, l2 = ax2.get_legend_handles_labels()
    ax1.legend(h1+h2, l1+l2, loc='best')
    return fig


if __name__ == '__main__':
    args = parse_arg()
    texts = wakati_tweets(load_tweets(args.FILES))
    dictionary = Dictionary.load_from_text(args.dictionary[0])
    corpus = MmCorpus(args.corpus[0])
    coherence_values = None
    perplexities = None
    for _ in range(args.repeat):
        c, p = compute_coherence_values(dictionary, corpus, texts, args.limit,
                                        args.start, args.step, args.coherence_measure)
        coherence_values = c if coherence_values is None else coherence_values + c
        perplexities = p if perplexities is None else perplexities + p
    coherence_values /= args.repeat
    perplexities /= args.repeat

    fig = plot_coherence_values(coherence_values, perplexities, args.limit, args.start, args.step)
    if args.save_fig is not None:
        fig.savefig(args.save_fig)
    else:
        fig.show()
        input("Press Enter")
