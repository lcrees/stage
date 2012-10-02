# -*- coding: utf-8 -*-

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
