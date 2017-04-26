#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Commandline script that helps you to stay healthy while working on a computer.
Reminds you to take breaks and do exercises.

usage:
./shell_fit --task="a task I'm working on" --project="the project the task belongs to"
'''
from os.path import expanduser
from datetime import datetime
from time import sleep
from subprocess import run, PIPE

import settings

import click


@click.group()
def cli():
    """ command container """
    pass

@click.command()
@click.option('--task', default='---', help='The task you\'re working on.')
@click.option('--project', default='---',
              help='The project you\'re working on. Think of it as a tag.')
def log(task, project):
    ''''''
    sf = ShellFit()
    sf.log(task, project)


@click.command()
def exercise():
    sf = ShellFit()
    sf.exercise()

cli.add_command(log)
cli.add_command(exercise)

class ShellFit(object):
    ''' write work and break entries to a file,
        notify when it is time for a break,
        suggest break exercises
    '''
    def __init__(self):
        self.history_file = expanduser(settings.history_file)
        self.exercises_file = expanduser(settings.exercises_file)
        self.work_time = settings.work_time * 60

    def exercise(self):
        exercise = self.select()
        print('\n')
        break_msg = '{}\t{}'.format('break', exercise)
        self.write(break_msg)
        
    def log(self, task, project):
        ''' orchestrate what the class does
        '''
        task_msg = '{}\t{}'.format(project, task)
        self.write(task_msg)

        self.progressbar(self.work_time, prefix='')
        self.notify(task)
        self.exercise()

    def write(self, msg):
        ''' write work and break entries to a file
            format:
            04.02.2017 14:04:20	a pj	a task
        '''
        timestamp = datetime.now().strftime('%d.%m.%Y %H:%M:%S')
        timestamped_msg = '{}\t{}\n'.format(timestamp, msg)
        with open(self.history_file, 'a') as hf:
            hf.write(timestamped_msg)
        print(timestamped_msg)

    def notify(self, msg):
        ''' use applescript to display a notification
        '''
        osascript_params = {
                            'title': 'shell-fit',
                            'subtitle': 'time for a break',
                            'soundname': 'Hero',
                            'notification': msg
                           }
        osascript_cmd = '\'display notification \"{notification}\" with title \"{title}\" subtitle \"{subtitle}\" sound name \"{soundname}\"\''.format(**osascript_params)
        cmd = 'osascript -e {}'.format(osascript_cmd)
        run(cmd, shell=True, check=True)

    def select(self):
        ''' use fzf to select a break exercise from a file
        '''
        cmd = 'cat {}|fzf'.format(self.exercises_file)
        # selection = run(['cat', self.exercises_file, '|', 'fzf'], shell=True, check=True, stdout=PIPE)
        selection = run(cmd, shell=True, check=True, stdout=PIPE)
        return selection.stdout.decode('utf-8')

    def progressbar(self, seconds, prefix='', suffix=''):
        ''' render a progressbar on the commandline
        '''
        def print_progressbar(iteration, total, decimals=1, length=100, fill='█'):
            """
            Call in a loop to create terminal progress bar
            @params:
                iteration   - Required  : current iteration (Int)
                total       - Required  : total iterations (Int)
                decimals    - Optional  : positive number of decimals in percent complete (Int)
                length      - Optional  : character length of bar (Int)
                fill        - Optional  : bar fill character (Str)
            """
            percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
            filled_length = int(length * iteration // total)
            bar = fill * filled_length + '-' * (length - filled_length)
            print('\r{} |{}| {}% {}'.format(prefix, bar, percent, suffix), end='\r')
            # Print New Line on Complete
            if iteration == total:
                print()

        # make a list
        items = list(range(0, seconds))
        i = 0
        l = len(items)

        # Initial call to print 0% progress
        print_progressbar(i, l, length=50)
        for item in items:
            # do stuff...
            sleep(1)
            # update progressbar
            i += 1
            seconds_left = l - i
            mins, secs = divmod(seconds_left, 60)
            suffix = '{:02d}:{:02d}'.format(mins, secs)

            print_progressbar(i, l, length=50)


if __name__ == '__main__':
    cli()
