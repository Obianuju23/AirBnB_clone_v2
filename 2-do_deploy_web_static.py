#!/usr/bin/python3
"""
Module that generates a .tgz archive from the 
web_static directory
"""
from os.path import exists
from fabric.api import env, run, put


env.hosts = ['100.26.253.193', '54.237.112.101']


def do_deploy(archive_path):
    """A function that distributes an archive file to a web server"""
    if not exists(archive_path):
        return False
    try:
        file_name = archive_path.split("/")[-1]
        no_ext = file_name.split(".")[0]
        path = "/data/web_static/releases/"
        put(archive_path, '/tmp/')
        run('mkdir -p {}{}/'.format(path, no_ext))
        run('tar -xzf /tmp/{} -C {}{}/'.format(file_name, path, no_ext))
        run('rm /tmp/{}'.format(file_name))
        run('mv {0}{1}/web_static/* {0}{1}/'.format(path, no_ext))
        run('rm -rf {}{}/web_static'.format(path, no_ext))
        run('rm -rf /data/web_static/current')
        run('ln -s {}{}/ /data/web_static/current'.format(path, no_ext))
        print("New version deployed!")
        flag = True
    except Exception as e:
        flag = False
    return flag
