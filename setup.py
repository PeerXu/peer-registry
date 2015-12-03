#! /usr/bin/env python2.7

from setuptools import setup
from setuptools import find_packages

requires = [
    "Flask==0.10.1",
    "PyYAML==3.11"
]

setup(
    name='peer_registry',
    description='',
    version='0.0.1',
    packages=find_packages(),
    author='Peer Xu',
    author_email='pppeerxu@gmail.com',
    install_requires=requires,
    entry_points={
        'console_scripts': ['peer-registry=peer_registry.scripts.main:main']
    }
)
