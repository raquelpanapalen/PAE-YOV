#!/usr/bin/env python3
import pyaudio
import wave
import pandas as pd
import argparse
import os
from playsound import playsound


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-i',
        '--input_file',
        dest='input_file',
        type=str,
        help='TSV input file',
        required=True,
    )
    parser.add_argument(
        '-o',
        '--output_db',
        dest='output_database',
        type=str,
        help='TSV output database name',
        required=True,
    )
    parser.add_argument(
        '-r', '--resume', dest='resume', type=int, help='index to resume'
    )
    return parser.parse_args()


class AudioRecorder:
    def __init__(self, input_file, output_database, resume):
        self.input_file = input_file
        self.resume = True if resume is not None else False
        self.database_name = output_database

        self.output_file = self.database_name + '_metadata'
        self.audio_filename = self.database_name + '_{}.wav'
        self.DB_DIR = os.path.join(
            os.path.dirname(__file__).replace('scripts', 'databases'),
            self.database_name
        )

        self.frames_per_buffer = 1024  # Record in chunks of 1024 samples
        self.format = pyaudio.paInt16  # 16 bits per sample
        self.channels = 1
        self.rate = 96000  # Record at 96000 samples per second
        self.p = pyaudio.PyAudio()
        self.stream = None
        self.last_audio = None
        self.index = resume if resume is not None else -1
        self.data_out = set()

        if not os.path.exists(self.DB_DIR):
            # Create a new directory because it does not exist
            os.makedirs(self.DB_DIR)

        # Menu options
        self.options = {
            '1': ('Record new audio', self.record),
            '2': ('Listen last recorded audio', self.listen_last),
            '3': ('Record last audio again', self.record),
            '4': ('Exit', self.exit),
        }
        self.exit_option = '4'
        print("Starting to record with row {} of TSV file".format(self.index + 1))

    def list_devices(self):
        for i in range(self.p.get_device_count()):
            print(f'Device {i} -> name: {self.p.get_device_info_by_index(i)["name"]}')

    def record(self):
        sentence = self.df.iloc[self.index]['sentence']
        print('*' * 100)
        print('Index %05d: \t %s' % (self.index, sentence))
        print('*' * 100)
        input("Press ENTER to start recording (and Ctrl+C to finish)")
        # Create an empty list for audio recording
        frames = []
        self.stream = self.p.open(
            format=self.format,
            channels=self.channels,
            rate=self.rate,
            input=True,
            frames_per_buffer=self.frames_per_buffer,
        )

        try:
            while True:
                # Record data audio data
                data = self.stream.read(self.frames_per_buffer)
                # Add the data to a buffer (a list of chunks)
                frames.append(data)
        except KeyboardInterrupt:
            pass

        # Stop and close the stream
        self.stream.stop_stream()
        self.stream.close()

        # Save the recorded data as a WAV file
        filename = os.path.join(self.DB_DIR, self.audio_filename.format(self.index))
        wf = wave.open(filename, 'wb')
        wf.setnchannels(self.channels)
        wf.setsampwidth(self.p.get_sample_size(self.format))
        wf.setframerate(self.rate)
        wf.writeframes(b''.join(frames))
        wf.close()

        # Add metadata to data_out
        self.data_out.add((self.database_name + '_%05d' % self.index, sentence))

    def listen_last(self):
        filename = os.path.join(self.DB_DIR, self.audio_filename.format(self.index))
        playsound(filename)

    def read_option(self):
        print('Select an option:')
        for key in sorted(self.options):
            print('{}) {}'.format(key, self.options[key][0]))
        while (a := input('Option: ')) not in self.options:
            print('ERROR: Incorrect option, try again.')
        return a

    def execute_option(self, option):
        if option in ['2', '3'] and self.index == -1:
            print('ERROR: No audios in the DB.')
            return
        elif option == '1' and self.index + 1 >= self.df.shape[0]:
            print('ERROR: No more sentences to record.')
            return
        elif option == '1':
            self.index += 1
        self.options[option][1]()

    def generate_menu(self):
        option = None
        while option != self.exit_option:
            option = self.read_option()
            self.execute_option(option)
            print()

    def run(self):
        self.df = pd.read_csv(self.input_file, sep='\t')
        self.generate_menu()

    def exit(self):
        # Terminate the PortAudio interface
        self.p.terminate()
        # Save new metadata
        if self.data_out:
            out_path = os.path.join(self.DB_DIR, self.output_file)
            df_out = pd.DataFrame(list(self.data_out))

            if self.resume:
                df1 = pd.read_csv(out_path + '.tsv', sep='\t', header=None)
                df_out = pd.concat([df1, df_out]).drop_duplicates().reset_index(drop=True)
                lines = [
                    '|'.join(tup)
                    for tup in list(df_out.itertuples(index=False, name=None))
                ]
            else:
                lines = ['|'.join(tup) for tup in self.data_out]

            with open(out_path + '.txt', 'w') as f:
                f.write('\n'.join(sorted(lines)))

            df_out.to_csv(out_path + '.tsv', sep='\t', header=False, index=False)
        print('Done recording! Bye :)')


if __name__ == '__main__':
    args = get_args()
    recorder = AudioRecorder(
        input_file=args.input_file,
        output_database=args.output_database,
        resume=args.resume
    )
    recorder.run()
