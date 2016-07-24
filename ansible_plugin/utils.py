# -*- UTF-8 -*-

import tempfile
from subprocess import Popen, PIPE

from cloudify import ctx
from cloudify import exceptions


def get_playbook_path(playbook):
    try:
        path_to_file = ctx.download_resource(playbook)
    except exceptions.HttpException as e:
        raise exceptions.NonRecoverableError(
            'Could not get playbook file: {}.'.format(str(e)))
    return path_to_file


def get_inventory_path(inventory):
    if not inventory:
        inventory.append(ctx.instance.host_ip)
    _, path_to_file = tempfile.mkstemp()
    with open(path_to_file, 'w') as f:
        for host in inventory:
            f.write('{0}\n'.format(host))
    return path_to_file


def run_command(command):
    try:
        run = Popen(command, stdout=PIPE)
    except Exception as e:
        raise exceptions.NonRecoverableError(
            'Unable to run command. Error {}'.format(str(e)))
    try:
        output = run.communicate()
    except Exception as e:
        raise exceptions.NonRecoverableError(
            'Unable to run command. Error {}'.format(str(e)))
    if run.returncode != 0:
        raise exceptions.NonRecoverableError(
            'Non-zero returncode. Output {}.'.format(output))
    return output
