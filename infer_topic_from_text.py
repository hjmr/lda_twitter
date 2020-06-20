import argparse

from utils import wakati_text
from gensim.corpora import Dictionary
from gensim.models import LdaModel


def parse_arg():
    args = argparse.ArgumentParser(description="infer topic from text.")
    args.add_argument("-m", "--model", type=str, nargs=1, help="specify LDA model.")
    args.add_argument("-d", "--dictionary", type=str, nargs=1, help="specify dictionary.")
    args.add_argument("TEXT", type=str, help="a text which infer topic for.")
    return args.parse_args()


if __name__ == "__main__":
    args = parse_arg()
    model = LdaModel.load(args.model[0])
    dictionary = Dictionary.load_from_text(args.dictionary[0])
    doc = wakati_text(args.TEXT)
    doc_vec = dictionary.doc2bow(doc)
    topics = model[doc_vec]
    topic_num_arr = [i for i, v in topics]
    topic_score_arr = [v for i, v in topics]
    topic_num = topic_num_arr[topic_score_arr.index(max(topic_score_arr))]
    topic_vec = model.show_topic(topic_num, 20)
    print(topic_vec)
