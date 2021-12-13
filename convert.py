# coding=utf-8

"""Encoding converter."""

import argparse


def arg_parse():
    parser = argparse.ArgumentParser(description="encoding converter")
    parser.add_argument("target_path", type=str, help="target file path")
    parser.add_argument("output_path", type=str, help="output file path")
    parser.add_argument("from_which", type=str, help="from which type")
    parser.add_argument("to_which", type=str, help="to which type")

    args = parser.parse_args()
    return args


def main():
    args = arg_parse()
    with open(args.target_path, 'r', encoding=args.from_which) as tf:
        lines = tf.readlines()
        with open(args.output_path, 'w', encoding=args.to_which) as of:
            for line in lines:
                of.write(line)


if __name__ == "__main__":
    main()
