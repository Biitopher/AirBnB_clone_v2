#!/usr/bin/python3
"""Deletes out-of-date archives, using the function do_clean"""


from fabric.api import env, run, lcd
from datetime import datetime

env.user = 'ubuntu'
env.hosts = ['34.229.69.25', '100.26.227.84']

def do_clean(number=0):
    number = int(number)
    if number < 1:
        number = 1

    with lcd('versions'):
        local('ls -t | tail -n +{} | xargs -I {} rm -f {}'.format(number + 1, '{}', '{}'))

    with cd('/data/web_static/releases'):
        run('ls -t | tail -n +{} | xargs -I {} rm -rf {}'.format(number + 1, '{}', '{}'))
