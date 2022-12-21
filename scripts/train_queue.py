#!/usr/bin/env python3
# Simple script for helping us with queueing the model training
# Author: aaaaluki
#
# DEPRECATED: This script does not work as intended, we are no longer using it,
# and you shouldn't either :)

import argparse
import os
import shlex
import subprocess
import time
import uuid
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Tuple

from script_utils import CC_YELLOW, CC_END


# Directory for the logs and configs
WORK_DIR = Path('/home/user/PAE-YOV/.train_queue')
COMMANDS_FILE = WORK_DIR / 'train_queue.conf'
LOG_FILE = WORK_DIR / 'train_queue.log'
INDEX_FILE = WORK_DIR / 'index.log'

# Time stuff
START_TIME = datetime.now()
TIMEDELTA_FMT = '{days}d, {hours:02d}:{minutes:02d}:{seconds:02d}'
WAIT_TIME = 10*60


def format_time(dt: datetime) -> str:
    """
    String formats the datetime object into our prefered date/time format

    :param dt: datetime object to format
    :type dt: datetime.datetime

    :return: Formated string
    :rtype: str
    """
    return dt.strftime('%Y-%m-%d %H:%M:%S.%f')[:-4]


def logln(line: str) -> None:
    """
    Prints and writes to the LOG_FILE the given line

    :param line: line/message to print and log
    :type line: str

    :return: None
    """
    dt = format_time(datetime.now())

    with open(LOG_FILE, 'a') as logfile:
        logfile.write(f'[{dt}] {line}\n')

    print(f'{CC_YELLOW}[{dt}]{CC_END} {line}')


def strfdelta(tdelta: timedelta, fmt: str) -> str:
    """
    String formats the timedelta object into our prefered date/time format

    :param tdelta: timedelta object to format
    :type tdelta: datetime.timedelta
    :param fmt: Output format with f-string style syntax
    :type fmt: str

    :return: Formated string
    :rtype: str
    """
    d = {"days": tdelta.days}
    d["hours"], rem = divmod(tdelta.seconds, 3600)
    d["minutes"], d["seconds"] = divmod(rem, 60)

    return fmt.format(**d)


def run_command(command: List[str]) -> Tuple[int, timedelta, str]:
    """
    Runns the given command and arguments

    Waits to return until the command has finished executing.
    Prints to stdout the output of the command while running.

    :param command: command with arguments to run
    :type command: list[str]

    :return: information about the command execution (exit code, execution time, stderr output)
    :rtype: (int, datetime.timedelta, str)
    """
    start_time = datetime.now()
    proc = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    logfile_name = f'stdout_{str(uuid.uuid4().hex)}.log'
    logfile_path = WORK_DIR / logfile_name
    with open(INDEX_FILE, 'a') as f:
        line = f'[{format_time(start_time)}] {logfile_name}: {" ".join(command)}\n'
        f.write(line)

    logfile = open(logfile_path, 'w')

    try:
        while proc.poll() is None:
            stdout_data = proc.stdout.readline().decode()
            print(stdout_data, end='')
            logfile.write(stdout_data)

    except KeyboardInterrupt:
        proc.kill()
        proc.wait()

    logfile.close()
    execution_time = datetime.now() - start_time
    exit_code = proc.poll()
    stderr_output = proc.stderr.read().decode()

    return (exit_code, execution_time, stderr_output)


def setup(args: argparse.Namespace) -> None:
    """
    Setup method

    Make sure the directories and files needed exists, if not create them.

    :param args: arguments returned by the argparse module
    :type args: argparse.Namespace

    :return: None
    """
    if not WORK_DIR.exists():
        os.makedirs(WORK_DIR)

    if not COMMANDS_FILE.exists():
        open(COMMANDS_FILE, 'w').close()

    if not LOG_FILE.exists():
        open(LOG_FILE, 'w').close()


def main(args: argparse.Namespace):
    """
    Main method

    :param args: arguments returned by the argparse module
    :type args: argparse.Namespace

    :return: None
    """
    # Running until:
    # a) The heat death of the universe
    # b) The server dies
    # c) Some witty boi presses Ctrl+C
    logln(f'It\'s been a while crocodile!')
    while True:
        with open(COMMANDS_FILE, 'r') as f_commands:
            commands = f_commands.readlines()

        # Skip blank lines on config file
        cmd = ''
        while len(commands) > 0 and cmd == '':
            cmd, *commands = commands
            cmd = cmd.strip()

        # If there are no commands on the queue wait some time
        if cmd == '':
            print(f'No command to execute, waiting {WAIT_TIME} s')
            try:
                time.sleep(WAIT_TIME)
            except KeyboardInterrupt:
                dt = datetime.now()
                logln('Ending because a witty boi pressed Ctrl+C ...')
                logln('See you later, alligator o/')
                logln(f'Total execution time: {strfdelta(dt - START_TIME, TIMEDELTA_FMT)}')
                return

            continue

        # Write the commands that are on the queue
        cmd = shlex.split(cmd)
        with open(COMMANDS_FILE, 'w') as f_commands:
            f_commands.seek(0)
            f_commands.writelines(commands)
            f_commands.truncate()

        # Execute given command and log output
        cmd_str = " ".join(cmd)
        logln(f'Running command: {cmd_str}')
        exit_code, execution_time, stderr_output = run_command(cmd)
        execution_time_str = strfdelta(execution_time, TIMEDELTA_FMT)
        logln(f'Command execution ended; Exit Code = {exit_code}; Execution Time = {execution_time_str};')
        if exit_code != 0:
            logln(f'An error occurred during command execution. Printing stderr output:\n{stderr_output}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Script in charge of the training queue')
    args = parser.parse_args()

    setup(args)
    main(args)

