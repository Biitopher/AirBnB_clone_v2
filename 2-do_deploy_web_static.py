#!/usr/bin/python3
"""Using function do deploy"""

from fabric.api import put, run, env
from os.path import exists
from datetime import datetime
env.hosts = ['34.229.69.25', '100.26.227.84']
env.user = 'ubuntu'


def do_deploy(archive_path):
    """Distributes an archive to the web servers."""
    if not exists(archive_path):
        return False

    try:
        if not exists(archive_path):
            return False

        file_name = archive_path.split("/")[-1]
        archive_name = file_name.split(".")[0]
        deployment_path = "/data/web_static/releases/"

        put(archive_path, '/tmp/')

        run('mkdir -p {}{}/'.format(deployment_path, archive_name))

        run('tar -xzf /tmp/{} -C {}{}/'.format(
            file_name, deployment_path, archive_name))
        run('rm /tmp/{}'.format(file_name))

        run('mv {0}{1}/web_static/* {0}{1}/'.format(
            deployment_path, archive_name))
        run('rm -rf {}{}/web_static'.format(deployment_path, archive_name))

        run('rm -rf /data/web_static/current')
        run('ln -s {}{}/ /data/web_static/current'.format(
            deployment_path, archive_name))

        print("New version deployed successfully!")
        return True
    except Exception as e:
        print("Deployment failed: {}".format(str(e)))
        return False
