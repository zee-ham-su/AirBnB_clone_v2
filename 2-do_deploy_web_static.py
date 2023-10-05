#!/usr/bin/python3
"""Distributes an archive to web servers using Fabric."""
from fabric.api import env, put, run
import os
from datetime import datetime
from pathlib import Path

env.user = 'ubuntu'
env.hosts = ['54.237.78.97', '54.90.37.186']
env.key_filename = '~/.ssh/id_rsa'


def do_deploy(archive_path):
    """Deploy the archive files to erb server"""
    try:
        if not (os.path.exists(archive_path)):
            return False

        # Upload the archive to /tmp/ directory on the server
        put(archive_path, '/tmp/')

        #  Extract the archive to /data/web_static/releases/
        timestamp = os.path.basename(archive_path)[-18:-4]
        run('sudo mkdir -p /data/web_static/\
        releases/web_static_{}/'.format(timestamp))

        # uncompress archive and delete .tgz
        run('sudo tar -xzf /tmp/web_static_{}.tgz -C \
        /data/web_static/releases/web_static_{}/'
            .format(timestamp, timestamp))

        # remove archive
        run('sudo rm /tmp/web_static_{}.tgz'.format(timestamp))

        # move contents into host web_static
        run('sudo mv /data/web_static/releases/web_static_{}/web_static/* \
        /data/web_static/releases/web_static_{}/'.format(timestamp, timestamp))

        # remove extraneous web_static dir
        run('sudo rm -rf /data/web_static/releases/\
        web_static_{}/web_static'
            .format(timestamp))

        # delete pre-existing sym link
        run('sudo rm -rf /data/web_static/current')

        # re-establish symbolic link
        run('sudo ln -s /data/web_static/releases/\
        web_static_{}/ /data/web_static/current'.format(timestamp))
    except Exception as e:
        print(f"An error occurred: {e}")
        return False

    # return True on success
    return True
