#!/usr/bin/python3
"""Using function d0 pack"""


from fabric.api import local
from datetime import datetime
import os


def do_pack():
    """Generates a .tgz archive from the web_static folder."""
 
    try:
        current_time = datetime.now().strftime('%Y%m%d%H%M%S')
        archive_path = "versions/web_static_{}.tgz".format(current_time)
        local("mkdir -p versions")
        local("tar -cvzf {} web_static".format(archive_path))
        return archive_path
    except Exception as e:
        return None
