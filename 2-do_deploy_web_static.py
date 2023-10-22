#!/usr/bin/python3
"""
Fabric script that distributes an archive to web servers.
"""

from datetime import datetime
from fabric.api import local, put, run, env
import os

env.hosts = ["100.27.11.52", "54.237.72.95"]
env.user = "ubuntu"


def do_pack():
    """
    Pack web_static into .tgz archive
    """
    local("mkdir -p versions")
    date = datetime.now().strftime("%Y%m%d%H%M%S")
    archive_path = "versions/web_static_{}.tgz".format(date)

    if local("tar -czvf {} web_static".format(archive_path)).succeeded:
        return archive_path
    return None

def do_deploy(archive_path):
    """
    Deploy an archive to web servers
    """
    if not os.path.exists(archive_path):
        return False

    try:
        archive_name = os.path.basename(archive_path)
        base_name = os.path.splitext(archive_name)[0]
        release_dir = "/data/web_static/releases/{}".format(base_name)
        put(archive_path, "/tmp/")
        run("sudo mkdir -p {}".format(release_dir))
        run("sudo tar -xzf /tmp/{} -C {}".format(archive_name, release_dir))
        run("sudo rm /tmp/{}".format(archive_name))

        run("sudo mv {}/web_static/* {}/".format(release_dir, release_dir))
        run("sudo rm -rf {}/web_static".format(release_dir))

        run("sudo rm -rf /data/web_static/current")
        run("sudo ln -s {} /data/web_static/current".format(release_dir))

        print("New version deployed!")
        return True
    except Exception as e:
        print("Error:", e)
        return False
