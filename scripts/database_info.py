#!/usr/bin/env python3
import argparse
import matplotlib.pyplot as plt
import numpy as np
import soundfile as sf
from datetime import timedelta
from matplotlib import colors
from matplotlib.offsetbox import AnchoredText
from pathlib import Path
from scipy import stats

from script_utils import *


IMG_DPI = 150


def get_char_info(file: str) -> dict[str, float]:
    pass

def main(args: argparse.Namespace) -> None:
    db_folder = Path(args.DATABASE)
    db_name = db_folder.name
    split_char = args.delimiter

    files_duration = np.array([])
    wav_files = db_folder.glob('**/*.wav')
    for file in wav_files:
        file_info = sf.info(file, verbose=False)
        files_duration = np.append(files_duration, file_info.duration)

    # Let's suppose all the files have the same characteristics
    files_channels = file_info.channels
    files_format = f'{file_info.format_info} [{file_info.format}]'
    files_subtype = f'{file_info.subtype_info} [{file_info.subtype}]'
    files_sample_rate = file_info.samplerate

    # Display general information
    total_duration = np.sum(files_duration)
    info('Displaying general information\n' \
         f'    Database name: {db_name}\n' \
         f'    Total duration: {timedelta(seconds=int(total_duration))}\n'
         f'    Sample rate: {files_sample_rate} Hz\n' \
         f'    Channels: {files_channels}\n' \
         f'    Format: {files_format}\n' \
         f'    Subtype: {files_subtype}')

    # Display statistics
    statistics = stats.describe(files_duration)
    info('Displaying statistics\n' \
         f'    Min: {statistics.minmax[0]:.2f} s\n' \
         f'    Max: {statistics.minmax[1]:.2f} s\n' \
         f'    Mean: {statistics.mean:.2f} s\n' \
         f'    Variance: {statistics.variance:.2f} s')

    # Make histogram
    max_duration = int(np.ceil(statistics.minmax[1]))
    fig, axs = plt.subplots(tight_layout=True)
    N, bins, patches = axs.hist(files_duration, bins=max_duration, zorder=10)
    axs.set_title(f'Histogram of {db_name}')
    axs.grid(which='both', zorder=0)
    axs.set_xlim(left=0, right=max_duration)
    axs.set_xlabel('Duration [s]')
    axs.set_ylabel('Count')

    # Put a text box with the main statistics on the plot
    box_text = 'Statictics\n' \
               f'Min: {statistics.minmax[0]:.2f} s\n' \
               f'Max: {statistics.minmax[1]:.2f} s\n' \
               f'Mean: {statistics.mean:.2f} s\n' \
               f'Variance: {statistics.variance:.2f} s'

    text_box = AnchoredText(box_text, frameon=True, loc=1, pad=0.5)
    plt.gca().add_artist(text_box)

    # Color the histogram
    if args.color_hist:
        fracs = N / N.max()
        norm = colors.Normalize(fracs.min(), fracs.max())
        for thisfrac, thispatch in zip(fracs, patches):
            color = plt.cm.viridis(norm(thisfrac))
            thispatch.set_facecolor(color)

    filename = f'{db_name}_histogram.png'
    plt.savefig(filename, dpi=IMG_DPI)
    info(f'Saved plot image as: {filename}')
    plt.show()


if __name__ == '__main__':
    parser = argparse.ArgumentParser('description')
    parser.add_argument('DATABASE', help='Database folder')
    parser.add_argument('-c', '--color_hist', action='store_true', help='Flag to colormap the histogram')
    args = parser.parse_args()

    main(args)

