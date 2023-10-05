#!/usr/bin/python3
"""Using function do deploy"""


from fabric.api import *
import os
from datetime import datetime

env.hosts = ['34.229.69.25', '100.26.227.84']
env.user = 'ubuntu'


def do_deploy(archive_path):
    """Distributes an archive to the web servers."""
    if not os.path.exists(archive_path):
        return False
    try:
        put(archive_path, '/tmp/')

        archive_filename = archive_path.split('/')[-1]
        folder_name = archive_filename.split('.')[0]
        remote_path = "/data/web_static/releases/{}".format(folder_name)

        sudo('mkdir -p {}'.format(remote_path))
        sudo('tar -xzf /tmp/{} -C {}'.format(archive_filename, remote_path))

        sudo('rm /tmp/{}'.format(archive_filename))

        sudo('rm -rf /data/web_static/current')
        sudo('ln -s {} /data/web_static/current'.format(remote_path))

        return True
    except Exception as e:
        print(e)
        return False
