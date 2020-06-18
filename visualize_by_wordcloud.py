import argparse
import math

from gensim.models import LdaModel

import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from wordcloud import WordCloud


def parse_arg():
    args = argparse.ArgumentParser(description="create WordCloud.")
    args.add_argument("-m", "--model", type=str, nargs=1,
                      help="specify LDA model.")
    args.add_argument("-f", "--font_path", type=str, default="NotoSansCJKjp-Light.otf",
                      help="specify font path.")
    args.add_argument("-c", "--color", type=str, default="darkblue",
                      help="specify color by name.")
    args.add_argument("-r", "--reverse_frequency", action="store_true",
                      help="to show words with smaller frequencies in larger fonts.")
    return args.parse_args()


def plot_wordcloud(model, font, color, reverse_frequency=False):
    def color_func(word, font_size, position, orientation, random_state, font_path):
        return color

    mask = np.array(Image.open("oval.png"))
    ncols = int(math.sqrt(model.num_topics))
    if ncols * ncols < model.num_topics:
        ncols += 1

    nrows = int(model.num_topics / ncols)
    if ncols * nrows < model.num_topics:
        nrows += 1

    fig, axs = plt.subplots(ncols=ncols, nrows=nrows)
    axs = axs.flatten()
    for a in axs:
        a.axis("off")

    for idx in range(model.num_topics):
        x = dict(model.show_topic(idx, 50))
        if reverse_frequency:
            for k in x.keys():
                x[k] = 1.0 - x[k]
        wc = WordCloud(
            font_path=font,
            background_color="white",
            color_func=color_func,
            mask=mask,
            random_state=0
        ).generate_from_frequencies(x)

        axs[idx].imshow(wc)
        axs[idx].set_title("Topic {}".format(idx))

    plt.tight_layout()
    return fig


if __name__ == "__main__":
    args = parse_arg()
    model = LdaModel.load(args.model[0])
    fig = plot_wordcloud(model, args.font_path, args.color, args.reverse_frequency)
    fig.show()
    input("Press Enter to finish.")
