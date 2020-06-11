import argparse
from pprint import pprint

from gensim.models import LdaModel


def parse_arg():
    args = argparse.ArgumentParser(description="check topics in LDA model.")
    args.add_argument("FILE", type=str,
                      help="specify LDA model.")
    return args.parse_args()


if __name__ == "__main__":
    args = parse_arg()
    model = LdaModel.load(args.FILE)
    pprint(model.print_topics(num_topics=-1))
