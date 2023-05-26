import re
import json
import argparse

import spacy

import normalize_text as nt

tokenizer = spacy.load("ja_ginza")

def parse_arg():
    args = argparse.ArgumentParser(description="make wakati texts from tweets.")
    args.add_argument("FILES", type=str, nargs="+", help="specify files.")
    return args.parse_args()


def show_tweets(tweets):
    for t in tweets:
        print("------------------------------------")
        print("tweet id: {}".format(t["id"]))
        print("screen_name: {}".format(t["user"]["screen_name"]))
        print("user id: {}".format(t["user"]["id"]))
        print(t["text"])


def load_tweets(files):
    tweets = []
    for fn in files:
        with open(fn, "r") as f:
            tweets.append(json.load(f))
    return tweets


def check_if_not_use(word, feature):
    yn = False
    POS_NOT_USED = [["名詞", "数詞"]]
    STOP_WORDS = []
    if word in STOP_WORDS:
        yn = True
    else:
        for p in POS_NOT_USED:
            if len(p) == 1:
                yn = yn or (p[0] == feature[0])
            else:
                yn = yn or (p[0] == feature[0] and p[1] == feature[1])
    return yn


def check_if_use(word, feature):
    yn = False
    POS_USED = [["名詞"], ["形容詞"], ["動詞"]]
    for p in POS_USED:
        if len(p) == 1:
            yn = yn or (p[0] == feature[0])
        else:
            yn = yn or (p[0] == feature[0] and p[1] == feature[1])
    return yn


def remove_urls(text):
    text = re.sub("https?://[\w!\?/\+\-_~=;\.,\*&@#\$%\(\)'\[\]]+", "", text)
    return text


def remove_screen_names(text):
    text = re.sub("@[A-Za-z0-9_]+", "", text)
    return text


def normalize_text(text):
    return remove_screen_names(nt.normalize_text(text))


def wakati_text(text):
    wakati = []
    doc = tokenizer(normalize_text(text))
    for sent in doc.sents:
        for token in sent:
            f = token.tag_.split("-")
            if check_if_use(token.lemma_, f) == True and check_if_not_use(token.lemma_, f) != True:
                w = token.lemma_
                if 1 < len(w):
                    wakati.append(w)
    return wakati


def wakati_texts(texts):
    wakati_texts = [wakati_text(t) for t in texts]
    return wakati_texts


def wakati_tweets(tweets):
    twitter_wakati_texts = wakati_texts([t["text"] for t in tweets])
    return twitter_wakati_texts


def test_for_tweets():
    args = parse_arg()
    tweets = load_tweets(args.FILES)
    texts = wakati_tweets(tweets)
    print(texts[0])

if __name__ == "__main__":
    print(wakati_text("今日はとても天気が良い。"))
