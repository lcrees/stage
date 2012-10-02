#! /usr/bin/env python
# -*- coding: utf-8 -*-
'''setup for stage'''

import sys
from os import getcwd
from os.path import join
from setuptools import setup, find_packages


def getversion(fname):
    '''Get `__version__` without importing.'''
    for line in open(fname):
        if line.startswith('__version__'):
            return '%s.%s.%s' % eval(line[13:].rstrip())

if float('%d.%s' % sys.version_info[:2]) < 2.7:
    reqs = 'reqs/requires-2.6.txt'
else:
    reqs = 'reqs/requires.txt'
install_requires = list(l for l in open(join(getcwd(), reqs), 'r').readlines())

setup(
    name='stage',
    version=getversion('stage/__init__.py'),
    description='Configuration over convention.',
    long_description=open(join(getcwd(), 'README.rst'), 'r').read(),
    keywords='configuration settings management pythonic',
    license='BSD',
    author='L. C. Rees',
    author_email='lcrees@gmail.com',
    url='https://bitbucket.org/lcrees/stage',
    packages=find_packages(),
    zip_safe=False,
    install_requires=install_requires,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: Implementation :: CPython',
        'Topic :: Software Development',
        'Topic :: Software Development :: Libraries',
    ],
)
