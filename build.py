# coding=utf-8

"""Build the language file (.pkl) packed with a dict, a vocab and a mapping. Then save it in lang/."""

import argparse
import pickle
import os


def arg_parse():
    parser = argparse.ArgumentParser(description="Vocabulary And Dictionary Builder")

    parser.add_argument("--vocab", type=str, default="data/vocab.txt", help="vocabulary path")
    parser.add_argument("--dict", type=str, default="data/dict.txt", help="pinyin-cc index dictionary path")
    parser.add_argument("--sub-char", type=str, default="0", help="define a substitute char")
    parser.add_argument("--save", type=str, default="lang/lang.pkl", help="output (.pkl) path")

    args = parser.parse_args()
    assert(os.path.exists(args.vocab))
    assert(os.path.exists(args.dict))
    assert(len(args.sub_char) <= 1)
    return args


def build_vocab(vocab_path):
    """Build the CC vocabulary from a single utf-8 .txt file into lib/vocab.pkl"""
    with open(vocab_path, encoding="utf-8") as f:
        lines = f.readlines()
    vocab = []
    for line in lines:
        for cc in line:
            vocab.append(cc)
    return vocab


def build_map(vocab):
    """Build a mapping (dictionary) from CCs to indices in vocabulary, saved as lib/map.pkl"""
    mapping = {}
    for i in range(len(vocab)):
        mapping[vocab[i]] = i
    return mapping


def build_dict(dict_path, mapping):
    """Build the pinyin-CC dictionary from a single utf-8 .txt file into lib/dict.pkl"""
    with open(dict_path, encoding="utf-8") as f:
        lines = f.readlines()
    dic = {}
    for line in lines:
        words = line.split()
        dic[words[0]] = []
        for cc in words[1:]:
            if cc not in mapping:
                continue
            dic[words[0]].append(cc)
    return dic


def main():
    args = arg_parse()

    vocab = build_vocab(args.vocab)
    if len(args.sub_char) > 0:
        vocab.append(args.sub_char)
    mapping = build_map(vocab)
    dic = build_dict(args.dict, mapping)
    if len(args.sub_char) > 0:
        dic["_"] = [args.sub_char]
    lang = {"vocab": vocab,
            "dict": dic,
            "map": mapping,
            "sub_char": args.sub_char}
    with open(args.save, "wb") as f:
        pickle.dump(lang, f)


if __name__ == "__main__":
    main()
