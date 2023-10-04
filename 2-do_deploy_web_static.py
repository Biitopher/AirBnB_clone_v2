#!/usr/bin/python3
"""Using function do deploy"""


from fabric.api import *
import os import exists
from datetime import datetime


env.hosts = ['34.229.69.25', '100.26.227.84']

def do_deploy(archive_path):
    """Distributes an archive to the web servers."""
    
    if not exists(archive_path):
        return False

    try:
        put(archive_path, '/tmp/')

        archive_filename = archive_path.split('/')[-1]
        folder_name = archive_filename.replace('.tgz', '')
        release_path = '/data/web_static/releases/{}/'.format(folder_name)
        run('mkdir -p {}'.format(release_path))
        run('tar -xzf /tmp/{} -C {}'.format(archive_filename, release_path))

        run('rm /tmp/{}'.format(archive_filename))

        current_link = '/data/web_static/current'
        run('rm -f {}'.format(current_link))

        run('ln -s {} {}'.format(release_path, current_link))

        print("New version deployed!")
        return True

    except Exception as e:
        return False
