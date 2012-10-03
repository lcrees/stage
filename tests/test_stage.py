# -*- coding: utf-8 -*-
'''Test stage.'''

from stuf.six import unittest


class Base(object):

    def test_conf_required(self):
        from stage.conf import Conf
        G = Conf(self.defaults, self.required).defaults
        self.assertEqual(G.LOG.NAME, 'root')
        self.assertEqual(G.LOG.LEVEL, 30)
        self.assertEqual(G.LOG.DATE, '%a, %d %b %Y %H:%M:%S')
        self.assertEqual(
            G.LOG.ENTRY,
            '%(levelname)-4s -- %(asctime)s -- %(name)s: %(message)s (%(module'
            ')s.%(funcName)s at %(lineno)s)',
        )
        self.assertRaises(AttributeError, lambda: G.LOG.STDOUT)
        self.assertTrue(G.STREAM.ENABLED)
        self.assertEqual(G.STREAM.LEVEL, 30)
        self.assertTrue(G.STREAM.STDOUT)
        self.assertRaises(AttributeError, lambda: G.STREAM.INTERVAL)
        self.assertFalse(G.ROTATE.ENABLED)
        self.assertEqual(G.ROTATE.PATH, '')
        self.assertEqual(G.ROTATE.BACKUPS, 1)
        self.assertEqual(G.ROTATE.INTERVAL, 'h')
        self.assertRaises(AttributeError, lambda: G.ROTATE.DATE)

    def test_conf_default(self):
        from stage.conf import Conf
        G = Conf(self.defaults, self.required).required
        self.assertFalse(G.SMTP.ENABLED)
        self.assertEqual(G.SMTP.TO, '')
        self.assertEqual(G.SMTP.SUBJECT, '')
        self.assertEqual(G.SMTP.HOST, '')
        self.assertEqual(G.SMTP.FROM, '')
        self.assertRaises(AttributeError, lambda: G.SMTP.METHOD)
        self.assertFalse(G.HTTP.ENABLED)
        self.assertEqual(G.HTTP.HOST, '')
        self.assertEqual(G.HTTP.URL, '')
        self.assertEqual(G.HTTP.METHOD, 'GET')
        self.assertRaises(AttributeError, lambda: G.HTTP.FROM)
        self.assertFalse(G.SYSLOG.ENABLED)
        self.assertEqual(G.SYSLOG.HOST, 'localhost')
        self.assertEqual(G.SYSLOG.PORT, 514)
        self.assertEqual(G.SYSLOG.FACILITY, 'LOG_USER')
        self.assertRaises(AttributeError, lambda: G.SYSLOG.TO)

    def test_conf_final(self):
        from stage.conf import Conf
        G = Conf(self.defaults, self.required).freeze()
        self.assertEqual(G.LOG.NAME, 'root')
        self.assertEqual(G.LOG.LEVEL, 30)
        self.assertEqual(G.LOG.DATE, '%a, %d %b %Y %H:%M:%S')
        self.assertEqual(
            G.LOG.ENTRY,
            '%(levelname)-4s -- %(asctime)s -- %(name)s: %(message)s (%(module'
            ')s.%(funcName)s at %(lineno)s)',
        )
        self.assertRaises(AttributeError, lambda: G.LOG.STDOUT)
        self.assertTrue(G.STREAM.ENABLED)
        self.assertEqual(G.STREAM.LEVEL, 30)
        self.assertTrue(G.STREAM.STDOUT)
        self.assertRaises(AttributeError, lambda: G.STREAM.INTERVAL)
        self.assertFalse(G.ROTATE.ENABLED)
        self.assertEqual(G.ROTATE.PATH, '')
        self.assertEqual(G.ROTATE.BACKUPS, 1)
        self.assertEqual(G.ROTATE.INTERVAL, 'h')
        self.assertRaises(AttributeError, lambda: G.ROTATE.DATE)
        self.assertFalse(G.SMTP.ENABLED)
        self.assertEqual(G.SMTP.TO, '')
        self.assertEqual(G.SMTP.SUBJECT, '')
        self.assertEqual(G.SMTP.HOST, '')
        self.assertEqual(G.SMTP.FROM, '')
        self.assertRaises(AttributeError, lambda: G.SMTP.METHOD)
        self.assertFalse(G.HTTP.ENABLED)
        self.assertEqual(G.HTTP.HOST, '')
        self.assertEqual(G.HTTP.URL, '')
        self.assertEqual(G.HTTP.METHOD, 'GET')
        self.assertRaises(AttributeError, lambda: G.HTTP.FROM)
        self.assertFalse(G.SYSLOG.ENABLED)
        self.assertEqual(G.SYSLOG.HOST, 'localhost')
        self.assertEqual(G.SYSLOG.PORT, 514)
        self.assertEqual(G.SYSLOG.FACILITY, 'LOG_USER')
        self.assertRaises(AttributeError, lambda: G.SYSLOG.TO)

    def test_env_defaults(self):
        from stage.conf import Env
        G = Env(self.defaults, self.required).defaults
        with G.LOG as LOG:
            self.assertEqual(LOG.NAME, 'root')
            self.assertEqual(LOG.get('REALNAME', 'root'), 'root')
            self.assertEqual(LOG.LEVEL, 30)
            self.assertEqual(LOG.DATE, '%a, %d %b %Y %H:%M:%S')
            self.assertEqual(
                LOG.ENTRY,
                '%(levelname)-4s -- %(asctime)s -- %(name)s: %(message)s '
                '(%(module)s.%(funcName)s at %(lineno)s)',
            )
            self.assertRaises(AttributeError, lambda: LOG.STDOUT)
        with G.STREAM as STREAM:
            self.assertTrue(STREAM.ENABLED)
            self.assertEqual(STREAM.LEVEL, 30)
            self.assertTrue(STREAM.STDOUT)
            self.assertRaises(AttributeError, lambda: STREAM.INTERVAL)
        with G.ROTATE as ROTATE:
            self.assertFalse(ROTATE.ENABLED)
            self.assertEqual(ROTATE.PATH, '')
            self.assertEqual(ROTATE.BACKUPS, 1)
            self.assertEqual(ROTATE.INTERVAL, 'h')
            self.assertRaises(AttributeError, lambda: ROTATE.DATE)
        from stage.conf import env
        G = env()
        with G.LOG as LOG:
            self.assertEqual(LOG.NAME, 'root')
            self.assertEqual(LOG.LEVEL, 30)
            self.assertEqual(LOG.DATE, '%a, %d %b %Y %H:%M:%S')
            self.assertEqual(
                LOG.ENTRY,
                '%(levelname)-4s -- %(asctime)s -- %(name)s: %(message)s '
                '(%(module)s.%(funcName)s at %(lineno)s)',
            )
            self.assertRaises(AttributeError, lambda: LOG.STDOUT)
        with G.STREAM as STREAM:
            self.assertTrue(STREAM.ENABLED)
            self.assertEqual(STREAM.LEVEL, 30)
            self.assertTrue(STREAM.STDOUT)
            self.assertRaises(AttributeError, lambda: STREAM.INTERVAL)
        with G.ROTATE as ROTATE:
            self.assertFalse(ROTATE.ENABLED)
            self.assertEqual(ROTATE.PATH, '')
            self.assertEqual(ROTATE.BACKUPS, 1)
            self.assertEqual(ROTATE.INTERVAL, 'h')
            self.assertRaises(AttributeError, lambda: ROTATE.DATE)

    def test_env_required(self):
        from stage.conf import Env
        G = Env(self.defaults, self.required).required
        with G.SMTP as SMTP:
            self.assertFalse(SMTP.ENABLED)
            self.assertEqual(SMTP.TO, '')
            self.assertEqual(SMTP.SUBJECT, '')
            self.assertEqual(SMTP.HOST, '')
            self.assertEqual(SMTP.FROM, '')
            self.assertRaises(AttributeError, lambda: SMTP.METHOD)
        with G.HTTP as HTTP:
            self.assertFalse(HTTP.ENABLED)
            self.assertEqual(HTTP.HOST, '')
            self.assertEqual(HTTP.URL, '')
            self.assertEqual(HTTP.METHOD, 'GET')
            self.assertRaises(AttributeError, lambda: HTTP.FROM)
        with G.SYSLOG as SYSLOG:
            self.assertFalse(SYSLOG.ENABLED)
            self.assertEqual(SYSLOG.HOST, 'localhost')
            self.assertEqual(SYSLOG.PORT, 514)
            self.assertEqual(SYSLOG.FACILITY, 'LOG_USER')
            self.assertRaises(AttributeError, lambda: SYSLOG.TO)
        from stage.conf import env
        G = env()
        with G.SMTP as SMTP:
            self.assertFalse(SMTP.ENABLED)
            self.assertEqual(SMTP.TO, '')
            self.assertEqual(SMTP.SUBJECT, '')
            self.assertEqual(SMTP.HOST, '')
            self.assertEqual(SMTP.FROM, '')
            self.assertRaises(AttributeError, lambda: SMTP.METHOD)
        with G.HTTP as HTTP:
            self.assertFalse(HTTP.ENABLED)
            self.assertEqual(HTTP.HOST, '')
            self.assertEqual(HTTP.URL, '')
            self.assertEqual(HTTP.METHOD, 'GET')
            self.assertRaises(AttributeError, lambda: HTTP.FROM)
        with G.SYSLOG as SYSLOG:
            self.assertFalse(SYSLOG.ENABLED)
            self.assertEqual(SYSLOG.HOST, 'localhost')
            self.assertEqual(SYSLOG.PORT, 514)
            self.assertEqual(SYSLOG.FACILITY, 'LOG_USER')
            self.assertRaises(AttributeError, lambda: SYSLOG.TO)

    def test_env_final(self):
        from stage.conf import Env
        G = Env(self.defaults, self.required).freeze()
        with G.LOG as LOG:
            self.assertEqual(LOG.NAME, 'root')
            self.assertEqual(LOG.get('REALNAME', 'root'), 'root')
            self.assertEqual(LOG.LEVEL, 30)
            self.assertEqual(LOG.DATE, '%a, %d %b %Y %H:%M:%S')
            self.assertEqual(
                LOG.ENTRY,
                '%(levelname)-4s -- %(asctime)s -- %(name)s: %(message)s '
                '(%(module)s.%(funcName)s at %(lineno)s)',
            )
            self.assertRaises(AttributeError, lambda: LOG.STDOUT)
        with G.STREAM as STREAM:
            self.assertTrue(STREAM.ENABLED)
            self.assertEqual(LOG.get('REALSTDOUT', False), False)
            self.assertEqual(STREAM.LEVEL, 30)
            self.assertTrue(STREAM.STDOUT)
            self.assertRaises(AttributeError, lambda: STREAM.DATE)
        with G.ROTATE as ROTATE:
            self.assertFalse(ROTATE.ENABLED)
            self.assertEqual(ROTATE.PATH, '')
            self.assertEqual(ROTATE.BACKUPS, 1)
            self.assertEqual(ROTATE.INTERVAL, 'h')
            self.assertRaises(AttributeError, lambda: ROTATE.LEVEL)
        with G.SMTP as SMTP:
            self.assertFalse(SMTP.ENABLED)
            self.assertEqual(SMTP.TO, '')
            self.assertEqual(SMTP.SUBJECT, '')
            self.assertEqual(SMTP.HOST, '')
            self.assertEqual(SMTP.FROM, '')
            self.assertRaises(AttributeError, lambda: SMTP.METHOD)
        with G.HTTP as HTTP:
            self.assertFalse(HTTP.ENABLED)
            self.assertEqual(HTTP.HOST, '')
            self.assertEqual(HTTP.URL, '')
            self.assertEqual(HTTP.METHOD, 'GET')
            self.assertRaises(AttributeError, lambda: HTTP.FROM)
        with G.SYSLOG as SYSLOG:
            self.assertFalse(SYSLOG.ENABLED)
            self.assertEqual(SYSLOG.HOST, 'localhost')
            self.assertEqual(SYSLOG.PORT, 514)
            self.assertEqual(SYSLOG.FACILITY, 'LOG_USER')
            self.assertRaises(AttributeError, lambda: SYSLOG.TO)
        from stage.conf import env
        G = env()
        with G.LOG as LOG:
            self.assertEqual(LOG.NAME, 'root')
            self.assertEqual(LOG.LEVEL, 30)
            self.assertEqual(LOG.DATE, '%a, %d %b %Y %H:%M:%S')
            self.assertEqual(
                LOG.ENTRY,
                '%(levelname)-4s -- %(asctime)s -- %(name)s: %(message)s '
                '(%(module)s.%(funcName)s at %(lineno)s)',
            )
            self.assertRaises(AttributeError, lambda: LOG.STDOUT)
        with G.STREAM as STREAM:
            self.assertTrue(STREAM.ENABLED)
            self.assertEqual(STREAM.LEVEL, 30)
            self.assertTrue(STREAM.STDOUT)
            self.assertRaises(AttributeError, lambda: STREAM.DATE)
        with G.ROTATE as ROTATE:
            self.assertFalse(ROTATE.ENABLED)
            self.assertEqual(ROTATE.PATH, '')
            self.assertEqual(ROTATE.BACKUPS, 1)
            self.assertEqual(ROTATE.INTERVAL, 'h')
            self.assertRaises(AttributeError, lambda: ROTATE.LEVEL)
        with G.SMTP as SMTP:
            self.assertFalse(SMTP.ENABLED)
            self.assertEqual(SMTP.TO, '')
            self.assertEqual(SMTP.SUBJECT, '')
            self.assertEqual(SMTP.HOST, '')
            self.assertEqual(SMTP.FROM, '')
            self.assertRaises(AttributeError, lambda: SMTP.METHOD)
        with G.HTTP as HTTP:
            self.assertFalse(HTTP.ENABLED)
            self.assertEqual(HTTP.HOST, '')
            self.assertEqual(HTTP.URL, '')
            self.assertEqual(HTTP.METHOD, 'GET')
            self.assertRaises(AttributeError, lambda: HTTP.FROM)
        with G.SYSLOG as SYSLOG:
            self.assertFalse(SYSLOG.ENABLED)
            self.assertEqual(SYSLOG.HOST, 'localhost')
            self.assertEqual(SYSLOG.PORT, 514)
            self.assertEqual(SYSLOG.FACILITY, 'LOG_USER')
            self.assertRaises(AttributeError, lambda: SYSLOG.TO)

    def test_with_defaults(self):
        from stage.conf import Context
        G = Context(self.defaults, self.required).defaults
        with G.STREAM as STREAM:
            self.assertTrue(STREAM.ENABLED)
            self.assertEqual(STREAM.LEVEL, 30)
            self.assertTrue(STREAM.STDOUT)
            self.assertRaises(AttributeError, lambda: STREAM.DATE)
        with G.LOG as LOG:
            self.assertEqual(LOG.get('REALNAME', 'root'), 'root')
            self.assertEqual(LOG.NAME, 'root')
            self.assertEqual(LOG.LEVEL, 30)
            self.assertEqual(LOG.DATE, '%a, %d %b %Y %H:%M:%S')
            self.assertEqual(
                LOG.ENTRY,
                '%(levelname)-4s -- %(asctime)s -- %(name)s: %(message)s '
                '(%(module)s.%(funcName)s at %(lineno)s)',
            )
            self.assertRaises(AttributeError, lambda: LOG.STDOUT)
        with G.ROTATE as ROTATE:
            self.assertFalse(ROTATE.ENABLED)
            self.assertEqual(ROTATE.PATH, '')
            self.assertEqual(ROTATE.BACKUPS, 1)
            self.assertEqual(ROTATE.INTERVAL, 'h')
            self.assertRaises(AttributeError, lambda: ROTATE.LEVEL)

    def test_with_required(self):
        from stage.conf import Context
        G = Context(self.defaults, self.required).required
        with G.SMTP as SMTP:
            self.assertEqual(SMTP.get('BCC', 'root@root.com'), 'root@root.com')
            self.assertFalse(SMTP.ENABLED)
            self.assertEqual(SMTP.TO, '')
            self.assertEqual(SMTP.SUBJECT, '')
            self.assertEqual(SMTP.HOST, '')
            self.assertEqual(SMTP.FROM, '')
            self.assertRaises(AttributeError, lambda: SMTP.METHOD)
        with G.HTTP as HTTP:
            self.assertFalse(HTTP.ENABLED)
            self.assertEqual(HTTP.HOST, '')
            self.assertEqual(HTTP.URL, '')
            self.assertEqual(HTTP.METHOD, 'GET')
            self.assertRaises(AttributeError, lambda: HTTP.FROM)
        with G.SYSLOG as SYSLOG:
            self.assertFalse(SYSLOG.ENABLED)
            self.assertEqual(SYSLOG.HOST, 'localhost')
            self.assertEqual(SYSLOG.PORT, 514)
            self.assertEqual(SYSLOG.FACILITY, 'LOG_USER')
            self.assertRaises(AttributeError, lambda: SYSLOG.TO)

    def test_with_final(self):
        from stage.conf import Context
        G = Context(self.defaults, self.required).freeze()
        with G.STREAM as STREAM:
            self.assertTrue(STREAM.ENABLED)
            self.assertEqual(STREAM.LEVEL, 30)
            self.assertTrue(STREAM.STDOUT)
        with G.LOG as LOG:
            self.assertEqual(LOG.NAME, 'root')
            self.assertEqual(LOG.LEVEL, 30)
            self.assertEqual(LOG.get('REALNAME', 'root'), 'root')
            self.assertEqual(LOG.DATE, '%a, %d %b %Y %H:%M:%S')
            self.assertEqual(
                LOG.ENTRY,
                '%(levelname)-4s -- %(asctime)s -- %(name)s: %(message)s '
                '(%(module)s.%(funcName)s at %(lineno)s)',
            )
            self.assertRaises(AttributeError, lambda: LOG.STDOUT)
        with G.ROTATE as ROTATE:
            self.assertFalse(ROTATE.ENABLED)
            self.assertEqual(ROTATE.PATH, '')
            self.assertEqual(ROTATE.BACKUPS, 1)
            self.assertEqual(ROTATE.INTERVAL, 'h')
            self.assertRaises(AttributeError, lambda: ROTATE.FACILITY)
        with G.SMTP as SMTP:
            self.assertFalse(SMTP.ENABLED)
            self.assertEqual(SMTP.TO, '')
            self.assertEqual(SMTP.SUBJECT, '')
            self.assertEqual(SMTP.HOST, '')
            self.assertEqual(SMTP.FROM, '')
            self.assertRaises(AttributeError, lambda: SMTP.INTERVAL)
        with G.HTTP as HTTP:
            self.assertFalse(HTTP.ENABLED)
            self.assertEqual(HTTP.HOST, '')
            self.assertEqual(HTTP.URL, '')
            self.assertEqual(HTTP.METHOD, 'GET')
            self.assertRaises(AttributeError, lambda: HTTP.FROM)
        with G.SYSLOG as SYSLOG:
            self.assertFalse(SYSLOG.ENABLED)
            self.assertEqual(SYSLOG.HOST, 'localhost')
            self.assertEqual(SYSLOG.PORT, 514)
            self.assertEqual(SYSLOG.FACILITY, 'LOG_USER')
            self.assertRaises(AttributeError, lambda: SYSLOG.TO)


class TestClassConf(Base, unittest.TestCase):

    def setUp(self):
        class defaults:
            class LOG:
                NAME = 'root'
                # log level
                LEVEL = 30  # warning
                # default log formats
                DATE = '%a, %d %b %Y %H:%M:%S'
                # log entry format
                ENTRY = (
                    '%(levelname)-4s -- %(asctime)s -- %(name)s: %(message)s'
                    ' (%(module)s.%(funcName)s at %(lineno)s)'
                )

            class STREAM:
                ENABLED = True
                # redirect STDOUT to the logger?
                STDOUT = True
                # sets log level STDOUT is displayed under
                LEVEL = 30  # warning

            class ROTATE:
                ENABLED = False
                # log file path
                PATH = ''
                # number of backups to keep
                BACKUPS = 1
                # interval to backup log file
                INTERVAL = 'h'
                ENCODING = None
                MODE = 'a'
                SIZE = 0

        class required:
            class SMTP:
                ENABLED = False
                # to email address
                TO = ''
                # email subject
                SUBJECT = ''
                # mail server
                HOST = ''
                # from email address
                FROM = ''
                AUTH = None
                TLS = None

            class HTTP:
                ENABLED = False
                # web server host
                HOST = ''
                # web url
                URL = ''
                # http method
                METHOD = 'GET'

            class SYSLOG:
                ENABLED = False
                # syslog host
                HOST = 'localhost'
                # syslog port
                PORT = 514
                # syslog facility
                FACILITY = 'LOG_USER'
        self.defaults = defaults
        self.required = required


class TestClassImportConf(Base, unittest.TestCase):

    def setUp(self):
        self.defaults = 'tests.classconf.defaults'
        self.required = 'tests.classconf.required'


class TestTwoDeep(Base, unittest.TestCase):

    def setUp(self):
        from stage.conf import With
        defaults = With()
        with defaults.LOG:
            defaults.NAME('root')
            # log level
            defaults.LEVEL(30)  # warning
            # default log formats
            defaults.DATE('%a, %d %b %Y %H:%M:%S')
            # log entry format
            defaults.ENTRY(
                '%(levelname)-4s -- %(asctime)s -- %(name)s: %(message)s (%(mo'
                'dule)s.%(funcName)s at %(lineno)s)'
            )
        with defaults.STREAM:
            defaults.ENABLED(True)
            # redirect STDOUT to the logger?
            defaults.STDOUT(True)
            # sets log level STDOUT is displayed under
            defaults.LEVEL(30)  # warning
        with defaults.ROTATE:
            defaults.ENABLED(False)
            # log file path
            defaults.PATH('')
            # number of backups to keep
            defaults.BACKUPS(1)
            # interval to backup log file
            defaults.INTERVAL('h')
            defaults.ENCODING(None)
            defaults.MODE('a')
            defaults.SIZE(0)
        required = With()
        with required.SMTP:
            required.ENABLED(False)
            # to email address
            required.TO('')
            # email subject
            required.SUBJECT('')
            # mail server
            required.HOST('')
            # from email address
            required.FROM('')
            required.AUTH(None)
            required.TLS(None)
        with required.HTTP:
            required.ENABLED(False)
            # web server host
            required.HOST('')
            # web url
            required.URL('')
            # http method
            required.METHOD('GET')
        with required.SYSLOG:
            required.ENABLED(False)
            # syslog host
            required.HOST('localhost')
            # syslog port
            required.PORT(514)
            # syslog facility
            required.FACILITY('LOG_USER')
        self.defaults = defaults
        self.required = required


class TestTwoDeepImport(Base, unittest.TestCase):

    def setUp(self):
        self.defaults = 'tests.twodeep.defaults'
        self.required = 'tests.twodeep.required'


class TestLocalConf(unittest.TestCase):

    def test_local_conf(self):
        from stage.conf import localconf

        class Foo(object):
            class Meta:
                # anchor link label
                anchor_link = ''
                fork_link = ''
                fts_index = ''
                index = ''
                reference_link = ''
                root_index = 'roots'
                slug_field = ''
                version_link = ''
                versioned = False

        class Bar(Foo):

            class Meta:
                fork_link = 'BAR_OF'
                fts_index = 'bar_text'
                index = 'cons'
                reference_link = 'BAR_NODE_OF'
                slug_field = 'slug'
                version_link = 'BAR_VERSION_OF'
                versioned = False

        class FooBar(Bar):

            class Meta:
                index = 'bar'
                anchor_link = 'foo'
                reference_link = 'FORK_NODE_OF'
                versioned = True

        this = localconf(FooBar)
        self.assertEqual(this.root_index, 'roots')
        self.assertTrue(this.versioned)
        self.assertEqual(this.index, 'bar')
        self.assertEqual(this.anchor_link,  'foo')
        self.assertEqual(this.fork_link,  'BAR_OF')
        self.assertEqual(this.fts_index,  'bar_text')
        self.assertEqual(this.reference_link,  'FORK_NODE_OF')
        self.assertEqual(this.slug_field,  'slug')
        self.assertEqual(this.version_link,  'BAR_VERSION_OF')
