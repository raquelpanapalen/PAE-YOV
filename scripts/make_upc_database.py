#!/usr/bin/env python3
import argparse
import codecs
import shutil
from tqdm import tqdm
from pathlib import Path

from script_utils import *


METADATA_SPLIT_CHAR = '|'
AUDIO_EXTENSION = '.wav'
METADATA_EXTENSION = '.mar'

INVALID_TRANSCRIPTION_CHARS = ['<', '>']


def extract_transcription(metadata_file_path: Path) -> str:
    transcription = ''

    metadata_file = codecs.open(metadata_file_path, 'r', 'iso-8859-1')
    reading_transcription = False
    for line in metadata_file.readlines():
        line = line.strip()

        if line.startswith('TXT'):
            reading_transcription = True

            transcription += line.lstrip('TXT: ').strip('"')
        
        elif reading_transcription:
            if not line.startswith('EXT'):
                # Not needed, I know it just feels nice
                reading_transcription = False  
                break

            transcription += line.lstrip('EXT: ').strip('"')

    return transcription.strip().replace(' .', '.')


def main(args: argparse.Namespace):
    output_database = Path(args.OUTPUT_DATABASE)
    database_root = Path(args.INPUT_DATABASE)
    if not output_database.exists():
        output_database.mkdir()

    elif not output_database.is_dir():
        error('Output database is not a folder')

    metadata_files = sorted(list(database_root.glob(f'**/*{METADATA_EXTENSION}')))

    output_metadata_file_path = output_database / 'metadata.txt'
    output_metadata_file = open(output_metadata_file_path, 'w')

    for metadata_file in tqdm(metadata_files):
        transcription = extract_transcription(metadata_file)

        # Skip files with invalid characters
        skip_file = False
        for char in INVALID_TRANSCRIPTION_CHARS:
            if char in transcription:
                skip_file = True
                break

        if skip_file:
            continue

        # Replace the metadata file extension for the audio file one
        # It's not pretty, I know
        audio_file = Path(metadata_file.as_posix().rstrip(METADATA_EXTENSION) + AUDIO_EXTENSION)

        # Log onto the new metadata file
        output_metadata_file.write(audio_file.stem + METADATA_SPLIT_CHAR + transcription + '\n')

        # Copy audio file
        output_audio_file = output_database / audio_file.name
        shutil.copyfile(audio_file, output_audio_file)


    output_metadata_file.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('INPUT_DATABASE', type=str,
                        help='Database root folder with the database')
    parser.add_argument('OUTPUT_DATABASE', type=str,
                        help='Database with our format')
    args = parser.parse_args()

    main(args)
