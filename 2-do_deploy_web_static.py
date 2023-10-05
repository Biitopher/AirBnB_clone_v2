#!/usr/bin/python3
"""Using function do deploy"""


from fabric.api import *
import os
from datetime import datetime

env.hosts = ['34.229.69.25', '100.26.227.84']
env.user = 'Ubuntu'


def do_deploy(archive_path):
    """Distributes an archive to the web servers."""
    if not os.path.exists(archive_path):
        return False
    filename = archive_path.split('/')[-1]

    no_tgz = '/data/web_static/releases/' + "{}".format(filename.split('.')[0])
    tmp = "/tmp/" + filename

    try:
        put(archive_path, "/tmp/")
        sudo("mkdir -p {}/".format(no_tgz))
        sudo("tar -xzf {} -C {}/".format(tmp, no_tgz))
        sudo("rm {}".format(tmp))
        sudo("mv {}/web_static/* {}/".format(no_tgz, no_tgz))
        sudo("rm -rf {}/web_static".format(no_tgz))
        sudo("rm -rf /data/web_static/current")
        sudo("ln -s {}/ /data/web_static/current".format(no_tgz))
        return True

    except Exception as e:
        return False
