# coding=utf-8

"""Print a pickle to see if anything went wrong"""

import argparse
import pickle


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("target", type=str, help="target file path")
    parser.add_argument("num", type=int, default="10", help="if pickle is a list, set a num limit")
    args = parser.parse_args()

    with open(args.target, "rb") as f:
        obj = pickle.load(f)

    for item in obj[:args.num]:
        print(item)


if __name__ == "__main__":
    main()