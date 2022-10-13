#!/usr/bin/env python
import argparse
import os
import sys
from typing import Type

from script_utils import *


SPLIT_CHAR = '|'
LEGAL_ENDINGS = '.,;'


def process_file(input_path: str, output_path: str) -> None:
    with open(input_path, 'r') as f_in, open(output_path, 'w') as f_out:
        info(f'Reading from "{input_path}" and writing to "{output_path}"')
        for line in f_in.readlines():
            parts = line.strip().split(SPLIT_CHAR)
            out_line = parts[0]
            for p in parts[1:]:
                if p[-1] not in LEGAL_ENDINGS:
                    p += LEGAL_ENDINGS[0]

                out_line += SPLIT_CHAR + p

            f_out.write(out_line + '\n')


def main(args: Type[argparse.Namespace]):
    input_path = args.INPUT
    output_path = args.OUTPUT
    
    if os.path.isdir(input_path):
        error('Input file is a directory!')

    if os.path.exists(output_path):
        warn('Output file exists, overwriting!')

    SPLIT_CHAR = args.split_char
    process_file(input_path, output_path)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('INPUT', type=str, help='Input file')
    parser.add_argument('OUTPUT', type=str, help='Output file')
    parser.add_argument('-s', '--split_char', type=str, help='Delimiter char on the input/output files')
    args = parser.parse_args()

    main(args)

