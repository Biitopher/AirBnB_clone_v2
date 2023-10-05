#!/usr/bin/python3
"""Creates and distributes an archive to your web servers, using function deploy"""


from fabric.api import local, put, run, env
from os.path import exists

env.hosts = ['<IP web-01>', '<IP web-02>']  # Replace with your server IPs
env.user = '<your-ssh-username>'  # Replace with your SSH username

def do_pack():
    """Generates a .tgz archive from the web_static folder."""
    
    if not os.path.exists('versions'):
        os.makedirs('versions')
    now = datetime.now()
    archive_name = 'web_static_{}.tgz'.format(
        now.strftime('%Y%m%d%H%M%S')
    )
    tar_command = 'tar -cvzf versions/{} web_static'.format(archive_name)
    result = local(tar_command)
    if result.succeeded:
        return 'versions/{}'.format(archive_name)
    else:
        return None



def deploy():
    """Deploy an archive to the web servers"""
    archive_path = do_pack()
    
    if not archive_path:
        return False

    return do_deploy(archive_path)
