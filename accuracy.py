# coding=utf-8

"""Compute accuracy of an output file with ground truth."""

import argparse
import os


def arg_parser():
    parser = argparse.ArgumentParser(description="Compute Accuracy")

    parser.add_argument("-o", "--output", type=str, default="output/test.txt", help="output file path")
    parser.add_argument("-gt", "--ground-truth", type=str, default="input/ground_truth.txt", help="output file path")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-s", "--by-sentence", action="store_true", default=True, help="compute by sentence")
    group.add_argument("-c", "--by-char", action="store_true", default=False, help="compute by char")

    args = parser.parse_args()
    assert os.path.exists(args.output)
    assert os.path.exists(args.ground_truth)
    return args


def main():
    args = arg_parser()

    with open(args.output, "r", encoding="utf-8") as f:
        predict = f.readlines()
    with open(args.ground_truth, "r", encoding="utf-8") as f:
        ground = f.readlines()

    if args.by_char:
        count = 0
        acc = 0
        for i in range(min(len(predict), len(ground))):
            for j in range(min(len(predict[i]), len(ground[i]))):
                count += 1
                if predict[i][j] == ground[i][j]:
                    acc += 1

    else:
        count = 0
        acc = 0
        for i in range(min(len(predict), len(ground))):
            count += 1
            flag = True
            for j in range(min(len(predict[i]), len(ground[i]))):
                if predict[i][j] != ground[i][j]:
                    flag = False
                    break
            if flag:
                acc += 1

    print("Accuracy:", acc / count)


if __name__ == "__main__":
    main()