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

def do_deploy(archive_path):
    """Distributes an archive to the web servers."""
    if not os.path.exists(archive_path):
        return False
    filename = archive_path.split('/')[-1]

    no_tgz = '/data/web_static/releases/' + "{}".format(filename.split('.')[0])
    tmp = "/tmp/" + filename

    try:
        put(archive_path, "/tmp/")
        run("mkdir -p {}/".format(no_tgz))
        run("tar -xzf {} -C {}/".format(tmp, no_tgz))
        run("rm {}".format(tmp))
        run("mv {}/web_static/* {}/".format(no_tgz, no_tgz))
        run("rm -rf {}/web_static".format(no_tgz))
        run("rm -rf /data/web_static/current")
        run("ln -s {}/ /data/web_static/current".format(no_tgz))
        return True

    except Exception as e:
        return False

def deploy():
    """Deploy an archive to the web servers"""
    archive_path = do_pack()
    
    if not archive_path:
        return False

    return do_deploy(archive_path)
