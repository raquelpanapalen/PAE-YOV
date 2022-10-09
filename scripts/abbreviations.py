#!/usr/bin/env python3
import sys
from pathlib import Path


# Source for the file: https://esadir.cat/convencions/tipografia/abreviacions/llistaabreviacions
INPUT_FILE = Path(__file__).parent / 'files/abbreviations_cat.txt.in'
OUTPUT_FILE = Path(__file__).parent / 'files/abbreviations_cat.txt'


# It's not the best code, but it works!
if __name__ == '__main__':
    # Display some important information
    print(f'Parsing "{INPUT_FILE}" into "{OUTPUT_FILE}"')

    # Remove empty lines from INPUT_FILE
    f = open(INPUT_FILE, 'r')
    abbreviation_list = [l.strip() for l in f.readlines() if l.strip() != ""]
    f.close()

    # Parse abbreviations
    abr_existents = list()
    for i in range(int(len(abbreviation_list) / 2)):
        meaning = abbreviation_list[2*i]
        abrs = [a.strip() for a in abbreviation_list[2*i+1].split('|')]

        for a in abrs:
            abr_existents.append((a, meaning))

    # Print sorted abbreviations
    with open(OUTPUT_FILE, 'w') as f:
        for k, v in sorted(abr_existents, key=lambda x: x[0]):
            f.write(f'("{k}", "{v}"),\n')

