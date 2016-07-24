# -*- coding:UTF-8 -*-

from setuptools import setup

setup(
    name='cloudify-ansible-plugin',
    version='1.1',
    author='dongkai',
    author_email='dongkai@beyondcent.com',
    description='Integrates with cloudify to deploy Ansible Playbooks',
    packages=['ansible_plugin'],
    license='LICENSE',
    zip_safe=False,
    install_requires=["cloudify-plugins-common==3.3a3", "ansible==1.8.2"]
)
