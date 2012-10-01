# -*- coding: utf-8 -*-
'''Pythonic configuration'''

from pprint import pformat
from inspect import isclass

from knife import lazyknife
from stuf.utils import lazyload
from stuf.desc import ResetMixin, lazy
from stuf import exhaustmap, frozenstuf
from stuf.six import intern, isstring, items

SLOTS = '_all _these _this'.split()


class _BaseFactory(object):

    '''Base configuration factory.'''

    def __repr__(self):  # pragma: no coverage
        return pformat(self._all)

    def __iter__(self):
        return items(self._all)

    def __enter__(self):
        return self


class ConfFactory(_BaseFactory):

    '''Configuration factory.'''

    def __init__(self):
        super(ConfFactory, self).__init__()
        self._all = {}
        self._these = self._this = None

    def __getattr__(self, key, getr=object.__getattribute__):
        try:
            return getr(self, key)
        except AttributeError:
            if not key.startswith('__'):
                key = intern(key)
                if self._these is None:
                    self._all[key] = self._these = {}
                elif self._this is None:
                    self._this = key
                return self

    def __exit__(self, e, f, b):
        self._these = self._this = None


class DeepConf(_BaseFactory):

    '''Deep (three level) configuration factory.'''

    __slots__ = SLOTS + '_other _out'.split()

    def __init__(self):
        super(DeepConf, self).__init__()
        # all configuration
        self._all = {}
        # everthing else
        self._these = self._this = self._other = self._out = None

    def __enter__(self):
        self._these = {}
        if self._out is None:
            self._all[self._this] = self._out = self._these
        self._other = self._this
        return self

    def __getattr__(self, key, getr=object.__getattribute__):
        try:
            return getr(self, key)
        except AttributeError:
            if not key.startswith('__'):
                self._this = intern(key.upper())
                return self

    def __call__(self, *args):
        if len(args) == 1:
            first = args[0]
            args = intern(first) if isstring(first) else first
        else:
            args = tuple(intern(a) for a in args if isstring(a))
        self._these[self._this] = args
        return self

    def __exit__(self, e, f, b):
        if self._these is not None:
            if self._out != self._these:
                self._out[self._other] = self._these
            self._these = None
        else:
            self._out = None


class FlatConf(ConfFactory):

    '''Flatter (two level deep) configuration factory.'''

    __slots__ = SLOTS

    def __call__(self, *args):
        self._these[self._this] = args[0] if len(args) == 1 else args
        self._this = None
        return self


class Conf(ResetMixin):

    '''Configuration manager.'''

    __slots__ = '_defaults _required'.split()

    def __init__(self, defaults=None, required=None):
        '''
        :keyword required: required settings
        :keyword defaults: default settings
        '''
        super(Conf, self).__init__()
        # configuration defaults
        self._defaults = {}
        self._load(self._defaults, defaults)
        # required configuration
        self._required = {}
        self._load(self._required, required)

    def __repr__(self):  # pragma: no coverage
        return pformat(self.freeze())

    def _load(self, destination, conf):
        if isstring(conf):
            conf = lazyload(conf)
        if isclass(conf):
            o = {}
            t = iter(lazyknife(conf).traverse().attrs('maps').merge())
            # setup base configuration
            first = next(t)
            first.pop('classname', None)
            update = o.update
            update(first)
            # setup nested configuration
            exhaustmap(lambda x: update({x.pop('classname', 'options'): x}), t)
            destination.update(o)
        elif isinstance(conf, _BaseFactory):
            destination.update(conf._all)

    @lazy
    def defaults(self):
        '''Get configuration default values.'''
        return frozenstuf(self._defaults.copy())

    @lazy
    def required(self):
        '''Get required configuration values.'''
        return frozenstuf(self._required.copy())

    def freeze(self, *args, **kw):
        '''Finalize configuration values.'''
        # 1. default options
        end = self._defaults.copy()
        # 2. final options
        end.update(*args, **kw)
        # 3. required options (last...they override everything)
        end.update(self._required.copy())
        return frozenstuf(end)
