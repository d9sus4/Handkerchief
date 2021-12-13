# coding=utf-8

"""Preprocess training data (utf-8) into lists (.pkl) of decorated strings."""

from pathlib import Path
import argparse
import glob
import json
import os
import pickle
import re
from symbol import decorated

rubbish = [r"原标题："]


def arg_parse():
    parser = argparse.ArgumentParser(description="training data preprocessor")

    parser.add_argument("-l", "--lang", type=str, default="lang/lang.pkl", help="load language pack")

    parser.add_argument("-t", "--target", dest="target", default="data/2016-*.txt", type=str, help="target file path, "
                                                                                                   "allow glob")
    parser.add_argument("--json", action="store_true", default=True, help="target is a json (or json list)")
    parser.add_argument("-k", "--keys", type=str, nargs="+", default=["html", "title"], help="if target is json, "
                                                                                             "indicate valid keys "
                                                                                             "here")
    parser.add_argument("-d", "--out-dir", dest="out_dir", type=str, default="train", help="output file directory")

    parser.add_argument("--pad", action="store_true", default=True, help="pad the sentences with substitute char")
    parser.add_argument("--clean", action="store_true", default=True, help="clean rubbish patterns")

    args = parser.parse_args()
    return args


def decorate(raw_str, mapping, sub_char, args):
    if args.clean:
        for i in rubbish:
            raw_str = re.sub(i, "", raw_str)

    deco = "".join(cc if cc in mapping else sub_char for cc in raw_str)
    if args.pad:
        deco = sub_char + deco + sub_char
    if len(sub_char) > 0:
        deco = re.sub(sub_char+"+", sub_char, deco)
    return deco


def main():
    args = arg_parse()

    with open(args.lang, "rb") as f:
        lang = pickle.load(f)
    mapping = lang["map"]
    sub_char = lang["sub_char"]
    target_list = glob.glob(args.target)
    for file in target_list:
        output = []
        with open(file, "r", encoding="utf-8") as f:
            print("Decorating data from file", file, "...")
            count = 0
            lines = f.readlines()
            for line in lines:
                if args.json:
                    json_data = json.loads(line)
                    for key in args.keys:
                        output.append(decorate(json_data[key], mapping, sub_char, args))
                else:
                    output.append(decorate(line, mapping, sub_char, args))
                count += 1
                if count % 10000 == 0:
                    print(count, "lines decorated.")
        with open(os.path.join(args.out_dir, Path(file).stem + ".pkl"), 'wb') as f:
            pickle.dump(output, f)


if __name__ == "__main__":
    main()
