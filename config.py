from string import Template

DIR_PATH = '/var/log'
CONF_DIR = '/etc/contrail/'

DEFAULT_DATE_FORMAT = '%Y/%m/%d %I:%M:%S %p'
DEFAULT_HANDLER = 'handlers.RotatingFileHandler'
DEFAULT_ARGS_HANDLER = Template(''' ('/var/log/contrail/${service}.log', 'a', 3000000, 10) ''')
DEFAULT_FORMAT = '%(asctime)s [%(name)s]: %(message)s'

MODULE_DICT = {'c': ['contrail-query-engine', 'contrail-dns', 'contrail-collector', 'contrail-control'],
               'p': ['contrail-api', 'contrail-schema', 'contrail-alarm-gen', 'contrail-analytics-api',
                     'contrail-discovery',
                     'contrail-topology', 'contrail-device-manager', 'contrail-snmp-collector', 'contrail-svc-monitor']}

COMMON_FORMAT_FLAGS_DICT = {
    "time": {"p": "%(asctime)s", "c": "%d"},
    "levelname": {"p": "%(levelname)s", "c": "%p"},
    "message": {"p": "%(message)s", "c": "%m"},
    "filename": {"p": "%(filename)s", "c": "%F"},
    "pathname": {"p": "%(pathname)s", "c": "%b"},
    "lineno": {"p": "%(lineno)s", "c": "%L"},
    "process": {"p": "%(process)d", "c": "%i"},
    "thread": {"p": "%(thread)d", "c": "%t"},
    "msecs": {"p": "%(msecs)d", "c": "%r"}
}

PYTHON_FORMAT_FLAGS_DICT = {
    "time": "%(asctime)s",
    "levelname": "%(levelname)s",
    "message": "%(message)s",
    "filename": "%(filename)s",
    "pathname": "%(pathname)s",
    "lineno": "%(lineno)s",
    "process": "%(process)d",
    "thread": "%(thread)d",
    "msecs": "%(msecs)d",
    "created": "%(created)f",
    "funcName": "%(funcName)s",
    "levelno": "%(levelno)s",
    "module": "%(module)s",
    "name": "%(name)s",
    "processName": "%(processName)s",
    "threadName": "%(threadName)s"
}

CPP_FORMAT_FLAGS_DICT = {
    "time": "%d",
    "levelname": "%p",
    "message": "%m",
    "filename": "%F",
    "pathname": "%b",
    "lineno": "%L",
    "process": "%i",
    "thread": "%t",
    "msecs": "%r",
    "domainname": "%H"
}
