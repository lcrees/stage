# -*- coding: utf-8 -*-
'''stage fabfile'''

from fabric.api import prompt, local, settings, env

regup = './setup.py register sdist --format=bztar,zip upload'
nodist = 'rm -rf dist'


def getversion(fname):
    '''
    Get the __version__ without importing.
    '''
    for line in open(fname):
        if line.startswith('__version__'):
            return '%s.%s.%s' % eval(line[13:])


def _promptup():
    with settings(warn_only=True):
        local('hg tag "%s"' % getversion('stage/__init__.py'))
        local('hg push ssh://hg@bitbucket.org/lcrees/stage')
        local('hg push github')


def _test(val):
    truth = val in ['py26', 'py27', 'py31', 'py32', 'py33', 'pypy']
    if truth is False:
        raise KeyError(val)
    return val


def tox_recreate():
    '''recreate stage test env'''
    prompt(
        'Enter testenv: [py26, py27, py31, py32, py33, pypy]',
        'testenv',
        validate=_test,
    )
    local('tox --recreate -e %(testenv)s' % env)


def releaser():
    '''stage releaser'''
    _promptup()
    local(regup)
    local(nodist)


def inplace():
    '''in-place stage'''
    with settings(warn_only=True):
        local('hg push ssh://hg@bitbucket.org/lcrees/stage')
        local('hg push github')
    local('./setup.py sdist --format=gztar,zip upload')
    local(nodist)
