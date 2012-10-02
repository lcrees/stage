==============================
Configuration over convention.
==============================

Classy configuration:

    >>> from stage import Conf
    >>> class defaults:
    ... class SMTP:
    ...     ENABLED = False
    ...     TO = ''
    ...     SUBJECT = ''
    ...     # mail server
    ...     HOST = ''
    ...     # from email address
    ...     FROM = ''
    ...     AUTH = None
    ...     TLS = None
    ... class HTTP:
    ...     ENABLED = False
    ...     # web server host
    ...     HOST = ''
    ...     # web url
    ...     URL = ''
    ...     # http method
    ...     METHOD = 'GET'
    ... class SYSLOG:
    ...     ENABLED = False
    ...     # syslog host
    ...     HOST = 'localhost'
    ...     # syslog port
    ...     PORT = 514
    ...     # syslog facility
    ...     FACILITY = 'LOG_USER'
    >>> class required:
    ... class LOG:
    ...     NAME = 'root'
    ...     # log level
    ...     LEVEL = 30  # warning
    ...     # default log formats
    ...     DATE = '%a, %d %b %Y %H:%M:%S'
    ...     # log entry format
    ...     ENTRY = (
    ...         '%(levelname)-4s -- %(asctime)s -- %(name)s: %(message)s'
    ...         ' (%(module)s.%(funcName)s at %(lineno)s)'
    ...     )
    ... class STREAM:
    ...     ENABLED = True
    ...     # redirect STDOUT to the logger?
    ...     STDOUT = True
    ...     # sets log level STDOUT is displayed under
    ...     LEVEL = 30  # warning
    ... class ROTATE:
    ...     ENABLED = False
    ...     # log file path
    ...     PATH = ''
    ...     # number of backups to keep
    ...     BACKUPS = 1
    ...     # interval to backup log file
    ...     INTERVAL = 'h'
    ...     ENCODING = None
    ...     MODE = 'a'
    ...     SIZE = 0
    >>> config = Conf(defaults, required).freeze()
    >>> config.LOG.NAME
    'root'
    >>> config.LOG.LEVEL
    30
    >>> config.LOG.DATE
    '%a, %d %b %Y %H:%M:%S'
    >>> config.STREAM.ENABLED
    True

Telepathic environment configuration:

    >>> from stage import TwoDeep, Env, env
    >>> required = TwoDeep()
    >>> with required.LOG:
    ... required.NAME('root')
    ... required.LEVEL(30)  # warning
    ... required.DATE('%a, %d %b %Y %H:%M:%S')
    ... required.ENTRY(
    ...     '%(levelname)-4s -- %(asctime)s -- %(name)s: %(message)s (%(mo'
    ...     'dule)s.%(funcName)s at %(lineno)s)'
    ... )
    >>> with required.STREAM:
    ... required.ENABLED(True)
    ... required.STDOUT(True)
    ... required.LEVEL(30)  # warning
    >>> with required.ROTATE:
    ... required.ENABLED(False)
    ... required.PATH('')
    ... required.BACKUPS(1)
    ... required.INTERVAL('h')
    ... required.ENCODING(None)
    ... required.MODE('a')
    ... required.SIZE(0)
    >>> defaults = TwoDeep()
    >>> with defaults.SMTP:
    ... defaults.ENABLED(False)
    ... defaults.TO('')
    ... defaults.SUBJECT('')
    ... defaults.HOST('')
    ... defaults.FROM('')
    ... defaults.AUTH(None)
    ... defaults.TLS(None)
    >>> with defaults.HTTP:
    ... defaults.ENABLED(False)
    ... defaults.HOST('')
    ... defaults.URL('')
    ... defaults.METHOD('GET')
    >>> with defaults.SYSLOG:
    ... defaults.ENABLED(False)
    ... defaults.HOST('localhost')
    ... defaults.PORT(514)
    ... defaults.FACILITY('LOG_USER')  
    >>> config = With(defaults, required).freeze()
    >>> with config.LOG as LOG:
    ... LOG.NAME
    ... 'root'
    ... LOG.LEVEL
    ... 30
    >>> with config.STREAM as STREAM:
    ... STREAM.LEVEL
    ... 30
    ... STREAM.STDOUT
    ... True
    >>> with config.ROTATE as ROTATE:
    ... ROTATE.ENABLED
    ... False
    ... ROTATE.BACKUPS
    ... 1
    ... ROTATE.INTERVAL
    ... 'h'

Meanwhile, in some other module...    

    >>> from stage import env
    >>> config = env()
    >>> with config.LOG as LOG:
    ... LOG.LEVEL
    ... 30
    ... LOG.DATE
    ... '%a, %d %b %Y %H:%M:%S'
    >>> with config.STREAM as STREAM:
    ... STREAM.ENABLED
    ... True
    ... STREAM.LEVEL
    ... 30
    ... STREAM.STDOUT
    ... True
    >>> with config.ROTATE as ROTATE:
    ... ROTATE.ENABLED
    ... False
    ... ROTATE.BACKUPS
    ... 1
    ... ROTATE.INTERVAL
    ... 'h'

Spooky.
