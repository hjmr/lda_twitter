import argparse
from pprint import pprint

from tweet_utils import load_tweets, wakati_tweets
from gensim.corpora import Dictionary
from gensim.models import LdaModel


def parse_arg():
    args = argparse.ArgumentParser(description="infer topic from text.")
    args.add_argument("-m", "--model", type=str, nargs=1, help="specify LDA model.")
    args.add_argument("-d", "--dictionary", type=str, nargs=1, help="specify dictionary.")
    args.add_argument("FILES", type=str, nargs="+", help="specify json files.")
    return args.parse_args()


def doc2vec(dictionary, text):
    doc_vec = dictionary.doc2bow(text)
    return doc_vec


def infer_topics(model, doc_vec):
    topics = model[doc_vec]
    return topics


def max_topic(model, topics):
    topic_num_arr = [i for i, v in topics]
    topic_score_arr = [v for i, v in topics]
    topic_num = topic_num_arr[topic_score_arr.index(max(topic_score_arr))]
    topic_vec = model.show_topic(topic_num, 20)
    return topic_num, topic_vec


if __name__ == "__main__":
    args = parse_arg()
    model = LdaModel.load(args.model[0])
    dictionary = Dictionary.load_from_text(args.dictionary[0])
    texts = wakati_tweets(load_tweets(args.FILES))
    for t, f in zip(texts, args.FILES):
        doc_vec = doc2vec(dictionary, t)
        topics = infer_topics(model, doc_vec)
        topic_num, topic_vec = max_topic(model, topics)
        pprint((f, topics, topic_num, topic_vec))
