# -*- coding: utf-8 -*-
'''Pythonic configuration'''

from os import environ
from pprint import pformat
from inspect import isclass
from base64 import b64encode, b64decode

from stuf import frozenstuf
from knife import lazyknife
from stuf.utils import lazyimport
from stuf.iterable import xpartmap
from stuf.desc import ResetMixin, lazy
from stuf.six import intern, isstring, items, pickle

_FACTORY_SLOTS = '_all _these _this'.split()
_ACCESS_SLOTS = '_defaults _required'.split()
_CONF_SLOTS = '_conf _this _current'.split()


class _BaseFactory(object):

    '''Base configuration factory.'''

    def __init__(self):
        super(_BaseFactory, self).__init__()
        # all configuration
        self._all = {}
        # context tracking
        self._these = self._this = None

    def __repr__(self):  # pragma: no coverage
        return pformat(self._all)

    def __iter__(self):
        for k, v in items(self._all):
            yield k, v

    def __enter__(self):
        return self


class ConfFactory(_BaseFactory):

    '''Core configuration factory.'''

    def __getattr__(self, key, getr=object.__getattribute__):
        try:
            return getr(self, key)
        except AttributeError:
            if not key.startswith('__'):
                key = intern(key)
                # configuration section
                if self._these is None:
                    self._all[key] = self._these = {}
                # configuration key
                elif self._this is None:
                    self._this = key
                return self

    def __exit__(self, e, f, b):
        # clear context
        self._these = self._this = None


class BaseConf(ResetMixin):

    '''Configuration manager.'''

    def __init__(self, defaults=None, required=None):
        '''
        :keyword required: required settings
        :keyword defaults: default settings
        '''
        super(BaseConf, self).__init__()
        # configuration defaults
        self._defaults = {}
        self._load(self._defaults, defaults)
        # required configuration
        self._required = {}
        self._load(self._required, required)

    def __repr__(self):  # pragma: no coverage
        return pformat(self.freeze())

    def __iter__(self):
        for k, v in self.freeze():
            yield k, v

    def _load(self, destination, conf):
        # load configuration
        if isstring(conf):
            # load import
            conf = lazyimport(conf)
        if isinstance(conf, _BaseFactory):
            # load configuration from factory
            destination.update(i for i in conf)
        elif isclass(conf):
            # load configuration from class
            newconf = {}
            xpartmap(
                lambda x, y: x({y.pop('classname', 'options'): y}),
                iter(lazyknife(conf).traverse().attrs('maps').merge()),
                newconf.update,
            )
            destination.update(newconf)

    @lazy
    def defaults(self):
        '''Get configuration default values.'''
        return self._wrapper(self._defaults.copy())

    @lazy
    def required(self):
        '''Get required configuration values.'''
        return self._wrapper(self._required.copy())

    def freeze(self, *args, **kw):
        '''Finalize configuration values.'''
        # 1. default options
        end = self._defaults.copy()
        # 2. final options
        end.update(*args, **kw)
        # 3. required options (last...they override everything)
        end.update(self._required.copy())
        return self._wrapper(end)


class With(ConfFactory):

    '''Factory for two-level deep configuration.'''

    __slots__ = _FACTORY_SLOTS

    def __call__(self, *args):
        # set value
        self._these[self._this] = args[0] if len(args) == 1 else args
        # clear key
        self._this = None
        return self


class Access(ResetMixin):

    '''Base configuration access.'''

    def __init__(self):
        super(Access, self).__init__()
        self._current = self._this = None

    def __repr__(self):  # pragma: no coverage
        return pformat(self._conf)

    def __getattr__(self, key, getr=object.__getattribute__):
        try:
            return getr(self, key)
        except AttributeError:
            if not key.startswith('__'):
                return self._resolve(key)

    def __exit__(self, e, f, b):
        self._current = None


class context(Access):

    '''Contextual configuration access.'''

    __slot__ = _ACCESS_SLOTS

    def __init__(self, conf):
        super(context, self).__init__()
        self._conf = frozenstuf(conf)

    def __enter__(self):
        # return configuration section
        self._current = self._this
        return self._this

    def _resolve(self, key):
        # fetch key from frozenconf
        self._this = getattr(self._conf, key)
        return self


class env(Access):

    '''Environment configuration access.'''

    __slots__ = _ACCESS_SLOTS + ['_join']

    def __init__(self, conf=None):
        super(env, self).__init__()
        self._join = join = '.'.join
        self._conf = envz = environ
        if conf is not None:
            dumps = pickle.dumps
            # populate os.environ
            for k, v in items(conf):
                for x, y in items(v):
                    envz[join((k, x))] = b64encode(dumps(y)).decode('utf-8')

    def __enter__(self):
        # make default key
        self._current = self._this
        return self

    def get(self, key, default=None):
        try:
            return self._resolve(key)
        except AttributeError:
            return default

    def _resolve(self, key):
        # store key
        self._this = key
        try:
            if self._current is None:
                self._current = key
                return self
            # get compound key from environment
            this = pickle.loads(b64decode(
                self._conf[self._join((self._current, key))].encode('latin-1')
            ))
        except AttributeError:
            # carry forward key
            self._current = key
            return self
        except KeyError:
            raise AttributeError(key)
        else:
            return this


class Context(BaseConf):

    '''Contextual configuration factory.'''

    __slots__ = _CONF_SLOTS
    _wrapper = context


class Env(BaseConf):

    '''Environment contextual configuration factory.'''

    __slots__ = _CONF_SLOTS
    _wrapper = env


class Conf(BaseConf):

    '''Attribute access configuration factory.'''

    __slots__ = _CONF_SLOTS
    _wrapper = frozenstuf
