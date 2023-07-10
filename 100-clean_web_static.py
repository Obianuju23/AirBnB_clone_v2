#!/usr/bin/python3
"""Module to delete out-of-date archives"""
import os
from fabric.api import *

"""setting the environment host for the servers"""
env.hosts = ['100.26.253.193', '54.237.112.101']


def clean_local(number=0):
    """cleans the pack"""
    lists = local('ls -1t versions', capture=True)
    lists = lists.split('\n')
    n = int(number)
    if n in (0, 1):
        n = 1
    for f in lists[n:]:
        local('rm versions/{}'.format(f))


def clean_remote(number=0):
    """cleans the data in webserver"""
    lists = run('ls -1t /data/web_static/releases')
    lists = lists.splitlines()
    n = int(number)
    if n in (0, 1):
        n = 1
    for f in lists[n:]:
        if f == 'test':
            continue
        run('rm -rf /data/web_static/releases/{}'.format(f))


def do_clean(number=0):
    """deletes older versions of data from web server"""
    clean_local(number)
    clean_remote(number)
