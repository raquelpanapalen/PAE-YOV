#!/usr/bin/env python3
import argparse
import glob
import re
import os
from pathlib import Path


PADDING_LENGTH = 4
CORRECT_METADATA = Path(__file__).parent / 'files/metadata.tsv'


def process_file(file: str) -> None:
    incorrect_metadata = Path(file)
    db_folder = incorrect_metadata.parent
    wav_files = glob.glob(os.path.join(db_folder, '*.wav'))

    # Sauce: https://stackoverflow.com/a/36202926
    wav_files.sort(key=lambda var:[int(x) if x.isdigit() else x for x in re.findall(r'[^0-9]|[0-9]+', var)])
    wav_num = len(wav_files)

    output_file = os.path.splitext(file)
    output_file = output_file[0] + '_fixed' + output_file[1]
    with open(CORRECT_METADATA, 'r') as correct, open(output_file, 'w') as out:
        lines = correct.readlines()[1:wav_num + 1]

        for i in range(wav_num):
            line = lines[i].strip()
            file = os.path.basename(wav_files[i])
            _, *transcriptions = line.split('\t')

            transcriptions = [file] + transcriptions
            out.write('|'.join(transcriptions) + '\n')


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('INPUT', help='Input DB folder')
    args = parser.parse_args()

    process_file(args.INPUT)

