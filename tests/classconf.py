# -*- coding: utf-8 -*-


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
