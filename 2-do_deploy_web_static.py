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

    try:
        put(archive_path, '/tmp/')
        
        archive_filename = os.path.basename(archive_path)
        folder_name = archive_filename[:-4]
        run('mkdir -p /data/web_static/releases/{}'.format(folder_name))
        run('tar -xzf /tmp/{} -C /data/web_static/releases/{}/'.format(
            archive_filename, folder_name))
        
        run('rm /tmp/{}'.format(archive_filename))
        
        run('rm -f /data/web_static/current')
        
        run('ln -s /data/web_static/releases/{} /data/web_static/current'.format(
            folder_name))
        
        print("New version deployed!")
        return True

    except Exception as e:
        return False
