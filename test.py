# coding=utf-8

"""Test model with an input file"""

import argparse
import os
import glob
import pickle
from pathlib import Path
from train import Model
from math import log


def arg_parse():
    parser = argparse.ArgumentParser(description="Test Model")

    parser.add_argument("-m", "--model", type=str, default="model/model.pkl", help="model pickle path")

    parser.add_argument("-l", "--lang", type=str, default="lang/lang.pkl", help="load language pack (.pkl)")

    io = parser.add_mutually_exclusive_group()
    io_path = io.add_argument_group()
    io_path.add_argument("-i", "--in-path", type=str, default="input/test.txt", help="input file path, allow glob")
    io_path.add_argument("-o", "--out-dir", type=str, default="output", help="output directory")
    io.add_argument("-c", "--thru-cmd", action="store_true", default=False, help="interact through cmd")

    # params
    parser.add_argument("-n", "--n-gram", type=int, default=2, help="apply n-gram model, downward compatible")
    parser.add_argument("-b", "--bias", type=float, default=1e-10, help="positive bias for all possibilities")
    parser.add_argument("--fp", action="store_true", default=False, help="apply front padding")
    parser.add_argument("--rp", action="store_true", default=False, help="apply rear padding")

    fine_tune = parser.add_mutually_exclusive_group()
    fine_tune.add_argument("--smooth", nargs="+", type=float, default=[], help="give n positive numbers to set "
                                                                               "smoothing weights for n-dim and less "
                                                                               "dim probabilities downwards")

    args = parser.parse_args()
    assert os.path.exists(args.model)
    assert os.path.exists(args.lang)
    assert 2 <= args.n_gram <= 4
    if args.smooth:
        assert len(args.smooth) == args.n_gram
        for i in range(0, args.n_gram):
            assert sum(args.smooth[-i:]) > 0
    assert args.bias > 0

    return args


def calc_prob(prefix, alt, model, args):
    """Compute the probability (actually, frequency) of prefix followed by alt."""
    """If prefix is empty, this returns the probability of alt itself."""

    def robust_divide(a, b):
        """robust a / b"""
        if a == 0:
            return 0
        elif b == 0:
            return 1
        else:
            return a / b

    result = 0.0
    n = len(prefix) + 1

    if not args.smooth:
        result = robust_divide(model[prefix[-n+1:] + alt], model[prefix[-n+1:]])

    else:
        weights = args.smooth[-n:]
        w_sum = sum(weights)
        for weight in weights:
            weight /= w_sum

        p = [robust_divide(model[alt], model[""])]
        for i in range(1, n):
            p.insert(0, robust_divide(model[prefix[-i:] + alt], model[prefix[-i:]]))
        for i in range(0, n):
            result += weights[i] * p[i]

    return result


def solve(words, model, dic, sub_char, args):
    """Translate words in form of a pinyin list."""
    if args.fp:
        words.insert(0, "_")
    if args.rp:
        words.append("_")
    n = args.n_gram

    prefixes = {"": 0.0}
    for pinyin in words:
        pruned = {}
        alts = dic[pinyin]
        for prefix in prefixes.keys():
            for alt in alts:
                now = prefix + alt
                key = now[-n + 1:]
                p = prefixes[prefix] + log(calc_prob(prefix[-n + 1:], alt, model, args) + args.bias)
                if key not in pruned:
                    pruned[key] = (now, p)
                else:
                    if p > pruned[key][1]:
                        pruned[key] = (now, p)
        prefixes = {}
        for key in pruned.keys():
            prefixes[pruned[key][0]] = pruned[key][1]
    result = max(prefixes, key=lambda i: prefixes[i])
    result = result.strip(sub_char)
    return result


def main():
    args = arg_parse()

    with open(args.model, "rb") as f:
        model = pickle.load(f)
    assert model[""] > 0
    assert model.dim >= args.n_gram

    with open(args.lang, "rb") as f:
        lang = pickle.load(f)
    vocab = lang["vocab"]
    dic = lang["dict"]
    mapping = lang["map"]
    sub_char = lang["sub_char"]

    if args.thru_cmd:
        print("You've chosen to interact with Handkerchief thru cmd.")
        while True:
            try:
                words = input().split(" ")
                print(solve(words, model, dic, sub_char, args))
            except Exception as e:
                print(e)
                break
    else:
        input_list = glob.glob(args.in_path)
        for file in input_list:
            results = []
            with open(file, "r", encoding="utf-8") as f:
                print("Now handkerchieving:", file)
                count = 0
                lines = f.readlines()
                for line in lines:
                    words = line.split()
                    results.append(solve(words, model, dic, sub_char, args))
                    count += 1
                    if count % 100 == 0:
                        print(count, "sentences processed.")
            with open(os.path.join(args.out_dir, Path(file).stem + ".txt"), 'w') as f:
                print("Now saving:", os.path.join(args.out_dir, Path(file).stem + ".txt"))
                for result in results:
                    f.write(result + '\n')


if __name__ == "__main__":
    main()
