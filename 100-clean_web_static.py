#!/usr/bin/python3
"""Deletes out-of-date archives, using the function do_clean"""

from fabric.api import env, run, lcd
from datetime import datetime
import os
env.user = 'ubuntu'
env.hosts = ['34.229.69.25', '100.26.227.84']


def do_clean(number=0):
     number = 1 if int(number) == 0 else int(number)

    archives = sorted(os.listdir("versions"))
    [archives.pop() for i in range(number)]
    with lcd("versions"):
        [local("rm ./{}".format(a)) for a in archives]

    with cd("/data/web_static/releases"):
        archives = run("ls -tr").split()
        archives = [a for a in archives if "web_static_" in a]
        [archives.pop() for i in range(number)]
        [run("rm -rf ./{}".format(a)) for a in archives]
