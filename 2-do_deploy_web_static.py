#!/usr/bin/python3
"""
Module that generates a .tgz archive from the web_static directory
"""
from os.path import exists
from fabric.api import env
from fabric.api import run
from fabric.api import put

"""setting the environment host for the servers"""
env.hosts = ['100.26.253.193', '54.237.112.101']


def do_deploy(archive_path):
    """A function that distributes an archive file to a web server"""
    if not exists(archive_path):
        return (False)
    try:
        file = archive_path.split("/")[-1]
        fn = file.split(".")[0]

    if put(archive_path, "/tmp/{}".format(file)).failed is True:
        return (False)

    if run("sudo rm -rf /data/web_static/releases/{}/".
            format(fn)).failed is True:
        return (False)

    if run("sudo mkdir -p /data/web_static/releases/{}/".
            format(fn)).failed is True:
        return (False)

    if run("sudo tar -xzf /tmp/{} -C /data/web_static/releases/{}/".
           format(file, fn)).failed is True:
        return (False)

    if run("sudo rm /tmp/{}".format(file)).failed is True:
        return (False)

    if run("sudo mv /data/web_static/releases/{}/web_static/* "
           "/data/web_static/releases/{}/".format(fn, fn)).failed is True:
        return (False)

    if run("sudo rm -rf /data/web_static/releases/{}/web_static".
           format(fn)).failed is True:
        return (False)

    if run("sudo rm -rf /data/web_static/current").failed is True:
        return (False)

    if run("sudo ln -s /data/web_static/releases/{}/ /data/web_static/current"
            .format(fn)).failed is True:
        return (False)

    return True
    except Exception as e:
    return false
