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

    put(archive_path, "/tmp/")
    folder = "/data/web_static/releases/web_static_20240406151125"
    run(f"mkdir -p {folder}")
    run(f"tar -xzf /tmp/web_static_20240406151125.tgz -C {folder}")
    run(f"mv {folder}/web_static/* {folder}/")
    run(f"rm -rf {folder}/web_static")
    run("rm /tmp/web_static_20240406151125.tgz")
    run("rm -rf /data/web_static/current")
    run(f"ln -s {folder} /data/web_static/current")

    return True
