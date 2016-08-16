# -*- coding:UTF-8 -*-
import os

from cloudify import ctx
from ansible_plugin import utils
from cloudify.decorators import operation


@operation
def ansible_playbook_ips(playbooks, inventorys=list(), **kwargs):
    """ Runs a playbook as part of a Cloudify lifecycle operation """

    inventory_path = utils.get_ips(inventorys)
    ctx.logger.info('Inventory path: {0}.'.format(inventory_path))

    for playbook in playbooks:
        playbook_path = utils.get_file(playbook)
        ctx.logger.info('Playbook path: {0}.'.format(playbook_path))
        command = ['ansible-playbook', '-i', inventory_path, playbook_path]
        ctx.logger.info('Running command: {0}.'.format(command))
        output = utils.run_command(command)
        ctx.logger.info('Command Output: {0}.'.format(output))
        ctx.logger.info('Finished running the Ansible Playbook.')


@operation
def ansible_playbook_file(playbooks, inventorys, **kwargs):
    """ Runs a playbook as part of a Cloudify lifecycle operation """

    for inventory in inventorys:
        inventory_path = utils.get_file(inventory)
        ctx.logger.info('Inventory path: {0}.'.format(inventory_path))

        for playbook in playbooks:
            playbook_path = utils.get_file(playbook)
            ctx.logger.info('Playbook path: {0}.'.format(playbook_path))
            command = ['ansible-playbook', '-i', inventory_path, playbook_path]
            ctx.logger.info('Running command: {0}.'.format(command))
            output = utils.run_command(command)
            ctx.logger.info('Command Output: {0}.'.format(output))
            ctx.logger.info('Finished running the Ansible Playbook.')


@operation
def ansible_playbook_module(module, playbook, inventorys,  **kwargs):
    """
    Runs a anisble module
    :param module:
    :param kwargs:
    :return:
    """
    name = module.split('.')[0]
    os.system('rm -rf /opt/' + name)
    path = utils.get_file(module)
    ctx.logger.info('Playbook module: {0}.'.format(path))
    command = ["tar", "zxvf", path, '-C', '/opt']
    output = utils.run_command(command)
    ctx.logger.info('Command Output: {0}.'.format(output))
    inventory = utils.get_inventory(playbook, inventorys, **kwargs)
    command = ['ansible-playbook', '-i', inventory, playbook]
    ctx.logger.info('Running command: {0}.'.format(command))
    output = utils.run_command(command)
    ctx.logger.info('Command Output: {0}.'.format(output))
    ctx.logger.info('Finished running the Ansible Playbook.')


@operation
def ansible_playbook_uninstall(playbook, inventorys,  **kwargs):
    """
    :param playbook:
    :param inventorys:
    :param kwargs:
    :return:
    """
    inventory = utils.get_inventory(playbook, inventorys, **kwargs)
    command = ['ansible-playbook', '-i', inventory, playbook]
    ctx.logger.info('Running command: {0}.'.format(command))
    output = utils.run_command(command)
    ctx.logger.info('Command Output: {0}.'.format(output))
    ctx.logger.info('Finished running the Ansible Playbook.')

