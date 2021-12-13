# coding=utf-8

"""Train your model and save it in model/."""

import argparse
import os
import glob
import pickle


class Model:
    def __init__(self, dim):
        self.elements = {"": 0}
        self.dim = dim

    def __getitem__(self, key):
        if key in self.elements:
            return self.elements[key]
        else:
            return 0

    def add(self, word):
        if word not in self.elements:
            self.elements[word] = 0
        self.elements[word] += 1
        if len(word) == 1:
            self.elements[""] += 1


def arg_parse():
    parser = argparse.ArgumentParser(description="Train Model")

    parser.add_argument("--data", type=str, default="train/2016-*.pkl", help="training data (.pkl) path, allow glob)")

    parser.add_argument("-n", "--n-gram", type=int, default=2, help="train an n-gram model")

    parser.add_argument("--save", type=str, default="model/model.pkl", help="output model pickle path")

    args = parser.parse_args()
    assert 2 <= args.n_gram <= 4
    return args


def load_train(train_path):
    train_data = []
    for file in glob.glob(train_path):
        with open(file, "rb") as f:
            data = pickle.load(f)
            train_data += data
    return train_data


def train(model, train_data):
    n = model.dim
    print("Now training a", n, "grams model.")

    count = 0
    for sentence in train_data:
        for k in range(1, n + 1):   # k-gram elements
            for i in range(len(sentence) - k + 1):
                word = ""
                for temp in range(i, i + k):
                    word += sentence[temp]
                model.add(word)
        count += 1
        if count % 10000 == 0:
            print(count, "sentences trained.")

    print("Training done!")


def main():
    args = arg_parse()

    model = Model(args.n_gram)
    train_data = load_train(args.data)  # default training db: 1121k+ data

    train(model, train_data)

    with open(args.save, "wb") as f:
        pickle.dump(model, f)


if __name__ == "__main__":
    main()
