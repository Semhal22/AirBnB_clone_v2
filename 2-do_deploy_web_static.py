#!/usr/bin/python3
"""
Fabric script that generates a .tgz archive from folder web_static
"""
from datetime import datetime
from fabric.api import *
import os

env.user = "ubuntu"
env.hosts = ["18.207.2.71", "54.157.142.152"]


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


def do_deploy(archive_path):
    """
    Distributes an archive to my webservers
    """
    if not os.path.exists(archive_path):
        return False

    full_name = archive_path.split('/')[1]
    name = full_name.split('.')[0]

    if put(archive_path, f"/tmp/{full_name}").failed:
        return False

    if run(f"rm -rf /data/web_static/releases/{name}/").failed:
        return False

    if run(f"mkdir -p /data/web_static/releases/{name}/").failed:
        return False

    if run(f"tar -xzf /tmp/{full_name} -C\
            /data/web_static/releases/{name}/").failed:
        return False
    if run(f"mv /data/web_static/releases/{name}/web_static/*\
            /data/web_static/releases/{name}/").failed:
        return False
    if run(f"rm -rf /data/web_static/releases/{name}/web_static").failed:
        return False
    if run(f"rm /tmp/{full_name}").failed:
        return False
    if run("rm -rf /data/web_static/current").failed:
        return False
    if run(f"ln -s /data/web_static/releases/{name}/\
            /data/web_static/current").failed:
        return False

    return True
