#!/usr/bin/python3
"""Using function do deploy"""


from fabric.api import *
import os import exists
from datetime import datetime

env.hosts = ['34.229.69.25', '100.26.227.84']
env.user = 'ubuntu'


def do_deploy(archive_path):
    """Distributes an archive to the web servers."""
    if not exists(archive_path):
        return False

    try:
        put(archive_path, "/tmp/")

        archive_filename = archive_path.split('/')[-1][:-4]

        run("mkdir -p /data/web_static/releases/{}/".format(archive_filename))

        run("tar -xzf /tmp/{} -C /data/web_static/releases/{}/"
            .format(archive_filename + ".tgz", archive_filename))

        run("rm /tmp/{}".format(archive_filename + ".tgz"))

        run("mv /data/web_static/releases/{}/web_static/* /data/web_static/releases/{}/"
            .format(archive_filename, archive_filename))

        run("rm -rf /data/web_static/releases/{}/web_static".format(archive_filename))

        run("rm -rf /data/web_static/current")

        run("ln -s /data/web_static/releases/{}/ /data/web_static/current"
            .format(archive_filename))

        print("New version deployed!")
        return True
    except Exception as e:
        return False

    if __name__ == "__main__":
    archive_path = do_pack()
    if archive_path:
        result = do_deploy(archive_path)
        if result:
            exit(0)
    exit(1)
