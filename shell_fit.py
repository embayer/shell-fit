#!/usr/bin/env python

'''
19.01.2017-14:20:31	rg ¯\_(ツ)_/¯
result = fzf.fuzz(query, input_path='path/to/file.txt')
'''
from os.path import expanduser
from datetime import datetime
from time import sleep
from subprocess import run, PIPE

import settings

import click


@click.command()
@click.option('--task', default='¯\_(ツ)_/¯', help='Number of greetings.')
@click.option('--project',
              help='The project you\'re working on. Think of it as a kind of tag.')
def log(task, project):
    ''''''
    sf = ShellFit()
    sf.log(task, project)


class ShellFit(object):
    def __init__(self):
        self.history_file = expanduser(settings.history_file)
        self.exercises_file = expanduser(settings.exercises_file)
        self.work_time = settings.work_time * 60

    def write(self, msg):
        timestamp = datetime.now().strftime('%d.%m.%Y %H:%M:%S')
        timestamped_msg = '{}\t{}\n'.format(timestamp, msg)
        with open(self.history_file, 'a') as hf:
            hf.write(timestamped_msg)
        print(timestamped_msg)

    def log(self, task, project):
        task_msg = '{}\t{}'.format(project, task)
        self.write(task_msg)

        self.progressbar(' 🐚 💪', self.work_time)
        self.notify(task)
        exercise = self.select()
        print('\n')
        break_msg = '{}\t{}'.format('break', exercise)
        self.write(break_msg)

    def select(self):
        cmd = 'cat {}|fzf'.format(self.exercises_file)
        # selection = run(['cat', self.exercises_file, '|', 'fzf'], shell=True, check=True, stdout=PIPE)
        selection = run(cmd, shell=True, check=True, stdout=PIPE)
        return selection.stdout.decode('utf-8')

    def countdown(self, timeout):
        while timeout:
            mins, secs = divmod(timeout, 60)
            timeformat = '{:02d}:{:02d}'.format(mins, secs)
            print(timeformat, end='\r')
            sleep(1)
            timeout -= 1

    def progressbar(self, task, seconds):
        # Print iterations progress
        def printProgressBar(iteration, total, prefix='', suffix='', decimals=1, length=100, fill= '█'):
            """
            Call in a loop to create terminal progress bar
            @params:
                iteration   - Required  : current iteration (Int)
                total       - Required  : total iterations (Int)
                prefix      - Optional  : prefix string (Str)
                suffix      - Optional  : suffix string (Str)
                decimals    - Optional  : positive number of decimals in percent complete (Int)
                length      - Optional  : character length of bar (Int)
                fill        - Optional  : bar fill character (Str)
            """
            percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
            filledLength = int(length * iteration // total)
            bar = fill * filledLength + '-' * (length - filledLength)
            print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end = '\r')
            # Print New Line on Complete
            if iteration == total:
                print()

        # make a list
        items = list(range(0, seconds))
        i = 0
        l = len(items)

        # Initial call to print 0% progress
        printProgressBar(i, l, prefix=task, suffix='', length=50)
        for item in items:
            # Do stuff...
            sleep(1)
            # Update Progress Bar
            i += 1
            seconds_left = l - i
            mins, secs = divmod(seconds_left, 60)
            timeformat = '{:02d}:{:02d}'.format(mins, secs)

            printProgressBar(i, l, prefix=task, suffix=timeformat, length=50)

    def notify(self, msg):
        osascript_params = {
                            'title': 'shell-fit',
                            'subtitle': 'time for a break',
                            'soundname': 'Hero',
                            'notification': msg
                           }
        osascript_cmd = '\'display notification \"{notification}\" with title \"{title}\" subtitle \"{subtitle}\" sound name \"{soundname}\"\''.format(**osascript_params)
        cmd = 'osascript -e {}'.format(osascript_cmd)
        run(cmd, shell=True, check=True)


if __name__ == '__main__':
    log()
