#!/usr/bin/python3
"""
Fabric script that deletes out-of-date archives
"""

from fabric.api import env, local, run
from datetime import datetime
from os.path import isfile
from fabric.contrib import files

env.user = 'ubuntu'
env.hosts = ['54.237.78.97', '54.90.50.227']
env.key_filename = '~/.ssh/id_rsa'


def do_clean(number=0):
    """Delete out-of-date archives
    Parameters:
        number (int): The number of recent archives
        to retain. Set to 0 or 1 to keep
        only the latest archive, or increase
        for more recent archives.
    Returns:
        None
    """
    number = int(number)

    if number < 0:
        return

    number = max(1, number)

    local('cd versions ; ls -t | tail -n +{} | xargs rm -rf'.format(
         number))
    path = '/data/web_static/releases'
    run('cd {} ; ls -t | tail -n +{} | xargs rm -rf'.format(
        path, number))
