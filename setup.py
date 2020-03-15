#! /usr/bin/python
# -*- coding: utf-8 -*-

from gro_cutter import common
from setuptools import setup, find_packages

setup(
    name="gro_cutter",
    version='1.1.1',
    description=common.package_description,
    url='https://github.com/wojciech-galan/gro_cutter',
    author='Wojciech Gałan',
    license='GNU GPL v3.0',
    install_requires=[
        'scipy',
        'matplotlib'
    ],
    packages=find_packages(),
    classifiers=[
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7'
    ],
    entry_points = {
        'console_scripts':[
            'gro_cutter = gro_cutter.__main__:main'
        ]

    }
)