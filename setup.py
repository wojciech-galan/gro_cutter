#! /usr/bin/python
# -*- coding: utf-8 -*-

from bozenka_walec import common
from setuptools import setup, find_packages

setup(
    name="viruses_classifier", #todo
    version='1.0.0',
    description=common.package_description,
    url='https://github.com/wojciech-galan/viruses_classifier', #todo
    author='Wojciech Gałan',
    license='GNU GPL v3.0',
    install_requires=[
        'scipy'
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
            'viruses_classifier = bozenka_walec.__main__:main' #todo
        ]

    }
)