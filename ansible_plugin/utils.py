# -*- coding:UTF-8 -*-
import os
import tempfile
import uuid
from subprocess import Popen, PIPE

from cloudify import ctx
from cloudify import exceptions


def get_file(playbook):
    try:
        path_to_file = ctx.download_resource(playbook)
    except exceptions.HttpException as e:
        raise exceptions.NonRecoverableError(
            'Could not get playbook file: {}.'.format(str(e)))
    return path_to_file


def get_ips(inventory):
    if not inventory:
        inventory.append(ctx.instance.host_ip)
    _, path_to_file = tempfile.mkstemp()
    with open(path_to_file, 'w') as f:
        for host in inventory:
            f.write('{0}\n'.format(host))
    return path_to_file


def get_inventory(playbook, inventory, **kwargs):
    _path = ''
    if playbook:
        # get every path
        info = playbook.split('/')[1:-1]
        # connect every path
        for _ in info:
            _path = _path + '/' + _
    if kwargs:
        var_path = _path + '/group_vars/'
        _var_path = var_path + info[-1] + '-servers'
        os.system('rm -rf ' + var_path + '*')
        os.system('touch ' + _var_path)
        with open(_var_path, 'w') as f:
            for key in kwargs['properties']:
                f.write('{0}: {1}\n'.format(key, kwargs['properties'][key]))
        f.close()
    if inventory:
        os.system('rm -rf ' + _path + '/hosts')
        path = '{}/hosts'.format(_path)
        os.system('touch ' + path)
        with open(path, 'w') as f:
            f.write('{0}\n'.format('[' + info[-1] + '-servers]'))
            f.write('{0}\n'.format(inventory))
        f.close()
    return path


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
