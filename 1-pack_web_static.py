#!/usr/bin/python3
"""
Fabric script that generates a .tgz archive from the contents of the web_static folder of your AirBnB Clone repo.
"""

from fabric.api import local
from datetime import datetime
import os

def do_pack():
    """
    Generates a .tgz archive from the contents of the web_static folder.
    Returns the archive path if successful, or None if there's an error.
    """
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    archive_name = "versions/web_static_{}.tgz".format(timestamp)

    if not os.path.exists("versions"):
        local("mkdir -p versions")

    try:
        local("tar -cvzf {} web_static".format(archive_name))
        return archive_name
    except Exception:
        return None

