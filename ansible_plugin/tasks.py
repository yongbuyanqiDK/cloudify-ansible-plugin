# -*- coding:UTF-8 -*-

from cloudify import ctx
from ansible_plugin import utils
from cloudify.decorators import operation


@operation
def ansible_playbook1(playbooks, inventory, **kwargs):
    """ Runs a playbook as part of a Cloudify lifecycle operation """

    inventory_path = utils.get_inventory_path(inventory)
    ctx.logger.info('Inventory path: {0}.'.format(inventory_path))

    for playbook in playbooks:
        playbook_path = utils.get_playbook_path(playbook)
        ctx.logger.info('Playbook path: {0}.'.format(playbook_path))
        command = ['ansible-playbook', '-i', inventory_path, playbook_path]
        ctx.logger.info('Running command: {0}.'.format(command))
        output = utils.run_command(command)
        ctx.logger.info('Command Output: {0}.'.format(output))
        ctx.logger.info('Finished running the Ansible Playbook.')

    return "install success"


@operation
def ansible_playbook(ip, name, state="latest", **kwargs):
    """
    run a command
    :param ip:
    :param name:
    :param state:
    :return:
    """
    if ip is None:
        ctx.logger.info("No IP")
    if name is None:
        ctx.logger.info("No Name")
    command = ['ansible', ip, '-m yum -a "name={0} state={1}"'.format(name, state)]
    ctx.logger.info('Running command: {0}.'.format(command))
    output = utils.run_command(command)
    ctx.logger.info('Command Output: {0}.'.format(output))
    ctx.logger.info('Finished running the Ansible Command.')




