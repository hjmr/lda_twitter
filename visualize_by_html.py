import argparse
from pprint import pprint

from gensim.corpora import Dictionary, MmCorpus
from gensim.models import LdaModel, TfidfModel

import pyLDAvis
import pyLDAvis.gensim  # don't skip this


def parse_arg():
    args = argparse.ArgumentParser(description="visualize LDA model.")
    args.add_argument("-c", "--corpus", type=str, nargs=1,
                      help="specify corpus file.")
    args.add_argument("-d", "--dictionary", type=str, nargs=1,
                      help="specify dictionary file.")
    args.add_argument("-m", "--model", type=str, nargs=1,
                      help="specify LDA model.")
    args.add_argument("-s", "--save_to_file", type=str,
                      help="speficy file which the HTML will be saved to.")
    args.add_argument("-t", "--use_tfidf", action="store_true",
                      help="use TF-IDF corpus.")
    args.add_argument("--method", type=str, default="pcoa",
                      help="specify a method for MDS by one from 'pcoa', 'mmds', or 'tsne'.")
    return args.parse_args()


if __name__ == "__main__":
    args = parse_arg()
    model = LdaModel.load(args.model[0])
    corpus = MmCorpus(args.corpus[0])
    if args.use_tfidf:
        tfidf = TfidfModel(corpus)
        corpus = tfidf[corpus]
    dictionary = Dictionary.load_from_text(args.dictionary[0])
    vis = pyLDAvis.gensim.prepare(model, corpus, dictionary, mds=args.method)
    if args.save_to_file is not None:
        pyLDAvis.save(vis, args.save_to_file)
    else:
        pyLDAvis.show(vis)
