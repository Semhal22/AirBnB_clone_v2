#!/usr/bin/python3
"""
Fabric script that generates a .tgz archive from folder web_static
"""
from datetime import datetime
from fabric.api import local


def do_pack():
    """
    Create archive(.tgz) from web_static folder
    """
    local("mkdir -p versions")
    now = datetime.now().strftime("%Y%m%d%H%M%S")
    archive_name = f"versions/web_static_{now}.tgz"
    result = local(f"tar -cvzf {archive_name} web_static")

    if result.failed:
        return None
    return archive_name
