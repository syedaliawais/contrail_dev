##imports
import keystoneclient.v2_0.client as ksclient
from os import environ as env
from logger import Logger
from config import *
from string import Template
from utils import *

file_logger = Logger('log-manager').get_logger_with_console()

''' C++ Property File Template '''

cpp_template = Template(''' 
log4cplus.rootLogger = DEBUG, logfile

log4cplus.appender.logfile = log4cplus::FileAppender

log4cplus.appender.logfile.File = /var/log/contrail/${service}.log
log4cplus.appender.logfile.Append = true
log4cplus.appender.logfile.ImmediateFlush = true
log4cplus.appender.logfile.layout = log4cplus::PatternLayout
log4cplus.appender.logfile.layout.ConversionPattern = $format

''')

''' Python Property File Template '''

python_template = Template('''
[loggers]
keys=root,$service

[handlers]
keys=root_handler,${service}_handler

[formatters]
keys=contrail_formatter

[logger_root]
level=NOTSET
handlers=root_handler

[logger_$service]
level=NOTSET
handlers=${service}_handler
qualname=$service_qualname
propagate=0


[handler_root_handler]
class=StreamHandler
level=NOTSET
formatter=contrail_formatter
args=()

[handler_${service}_handler]
class=$handler
args=$args
formatter=contrail_formatter

[formatter_contrail_formatter]

format = $format
datefmt=$dateformat
class=logging.Formatter 
''')


def authenticate_request():
    keystone = {}
    keystone['username'] = env['OS_USERNAME']
    keystone['password'] = env['OS_PASSWORD']
    keystone['auth_url'] = env['OS_AUTH_URL']
    keystone['tenant_name'] = env['OS_TENANT_NAME']
    try:
        kClient = ksclient.Client(**keystone)
        return True
    except Exception, e:
        file_logger.debug("Unable to authenticate with Keystone: %s", e)
        return False


class LogManager(object):
    def __init__(self, service, conf_file_path, prop_file_path, is_structured=None, log_format=None,
                 log_date_format=None, log_severity_level=None):
        self.__service = service
        self.__conf_file_path = conf_file_path
        self.__prop_file_path = prop_file_path
        self.__is_structured = is_structured
        self.__log_format = log_format
        self.__log_date_format = log_date_format
        self.__log_severity_level = log_severity_level


    def add_property_path_to_config_file(self, module_type):
        if module_type == 'p':
            ''' Telling contrail service to load new configurations from the generated file '''
            cfg = ConfigParser.RawConfigParser()
            try:
                cfg.read(self.__conf_file_path + self.__service + '.conf')
                cfg.set('DEFAULTS', 'logger_class', 'pysandesh.sandesh_logger.SandeshConfigLogger')
                cfg.set('DEFAULTS', 'logging_conf', self.__prop_file_path + self.__service + '-properties.conf')
                with open(self.__conf_file_path + self.__service + '.conf', 'wb') as configfile:
                    cfg.write(configfile)
            except Exception, e:
                file_logger.debug('Error in parsing file! Please validate the config file.')
        else:
            cfg = ConfigParser.RawConfigParser()
            try:
                cfg.read(self.__conf_file_path + self.__service + '.conf')
                cfg.set('DEFAULT', 'log_property_file',
                        self.__prop_file_path + self.__service + '-properties.properties')
                with open(self.__conf_file_path + self.__service + '.conf', 'wb') as configfile:
                    cfg.write(configfile)
            except Exception, e:
                file_logger.debug('Error in parsing file! Please validate the config file.')


    def change_python_logging_format(self):
        module_type = is_python_or_cpp(self.__service)
        if not property_file_exists(self.__prop_file_path, self.__service, module_type):
            formatted_format = log_format_formatter(self.__log_format, module_type)
            service_name = conv_service_name_from_hyphen_to_underscore(self.__service)
            if self.__log_date_format is None:
                finalized_prop = python_template.substitute(service=service_name, service_qualname=self.__service,
                                                            handler=DEFAULT_HANDLER,
                                                            args=DEFAULT_ARGS_HANDLER.substitute(
                                                                service=self.__service), format=formatted_format,
                                                            dateformat=DEFAULT_DATE_FORMAT)
                file_logger.debug('No DateFormat was specified! Using the Default Date Format: %s', DEFAULT_DATE_FORMAT)
            else:
                finalized_prop = python_template.substitute(service=service_name, service_qualname=self.__service,
                                                            handler=DEFAULT_HANDLER,
                                                            args=DEFAULT_ARGS_HANDLER.substitute(
                                                                service=self.__service), format=formatted_format,
                                                            dateformat=self.__log_date_format)
            write_template_to_file(self.__prop_file_path, self.__service, module_type, finalized_prop)
            # Telling contrail service to load new configurations from the generated file
            self.add_property_path_to_config_file(module_type)

        else:
            formatted_format = log_format_formatter(self.__log_format, module_type)
            service_name = conv_service_name_from_hyphen_to_underscore(self.__service)
            if self.__log_date_format is None:
                write_value_to_config_file(self.__prop_file_path, self.__service, 'formatter_contrail_formatter',
                                           'format', formatted_format)
            else:
                write_value_to_config_file(self.__prop_file_path, self.__service, 'formatter_contrail_formatter',
                                           'format', formatted_format)
                write_value_to_config_file(self.__prop_file_path, self.__service, 'formatter_contrail_formatter',
                                           'datefmt', self.__log_date_format)

    def change_cpp_logging_format(self):
        module_type = is_python_or_cpp(self.__service)
        if not property_file_exists(self.__prop_file_path, self.__service, module_type):
            formatted_format = log_format_formatter(self.__log_format, module_type)
            if self.__log_date_format is not None:
                splitted = formatted_format.split(' ')
                formatted_format = ''
                for s in splitted:
                    if s == '%d':
                        s = '%d{' + self.__log_date_format + '}'
                    formatted_format += s + ' '
            finalized_prop = cpp_template.substitute(service=self.__service, format=formatted_format)
            write_template_to_file(self.__prop_file_path, self.__service, module_type, finalized_prop)
            self.add_property_path_to_config_file(module_type)
        else:
            formatted_format = log_format_formatter(self.__log_format, module_type)
            if self.__log_date_format is not None:
                splitted = formatted_format.split(' ')
                formatted_format = ''
                for s in splitted:
                    if s == '%d':
                        s = '%d{' + self.__log_date_format + '}'
                    formatted_format += s + ' '
            write_value_to_property_file(self.__prop_file_path, self.__service, formatted_format)


    def disable_logs(self):
        module_type = is_python_or_cpp(self.__service)
        if module_type == 'c':
            cfg = ConfigParser.RawConfigParser()
            try:
                cfg.read(self.__conf_file_path + self.__service + '.conf')
                cfg.set('DEFAULT', 'log_disable', 1)
                with open(self.__conf_file_path + self.__service + '.conf', 'wb') as configfile:
                    cfg.write(configfile)
            except Exception, e:
                file_logger.debug('Error in parsing file! Please validate the config file.')

        else:
            service_name = conv_service_name_from_hyphen_to_underscore(self.__service)
            if property_file_exists(self.__prop_file_path, self.__service, module_type):
                cfg = ConfigParser.RawConfigParser()
                try:
                    cfg.read(self.__prop_file_path + self.__service + '-properties.conf')
                    cfg.set('handler_' + service_name + '_handler', 'class', 'NullHandler')
                    cfg.set('handler_' + service_name + '_handler', 'args', '()')
                    with open(self.__prop_file_path + self.__service + '-properties.conf', 'wb') as configfile:
                        cfg.write(configfile)
                except Exception, e:
                    file_logger.debug('Error in parsing file! Please validate the config file.')
            else:
                finalized_prop = python_template.substitute(service=service_name, service_qualname=self.__service,
                                                            handler='NullHandler', args='()', format=DEFAULT_FORMAT,
                                                            dateformat=DEFAULT_DATE_FORMAT)
                write_template_to_file(self.__prop_file_path, self.__service, module_type, finalized_prop)
                self.add_property_path_to_config_file(module_type)


    def enable_logs(self):
        module_type = is_python_or_cpp(self.__service)
        if module_type == 'c':
            cfg = ConfigParser.RawConfigParser()
            try:
                cfg.read(self.__conf_file_path + self.__service + '.conf')
                cfg.set('DEFAULT', 'log_disable', 0)
                with open(self.__conf_file_path + self.__service + '.conf', 'wb') as configfile:
                    cfg.write(configfile)
            except Exception, e:
                file_logger.debug('Error in parsing file! Please validate the config file.')
        else:
            if property_file_exists(self.__prop_file_path, self.__service, module_type):
                service_name = conv_service_name_from_hyphen_to_underscore(self.__service)
                cfg = ConfigParser.RawConfigParser()
                try:
                    cfg.read(self.__prop_file_path + self.__service + '-properties.conf')
                    cfg.set('handler_' + service_name + '_handler', 'class', DEFAULT_HANDLER)
                    cfg.set('handler_' + service_name + '_handler', 'args',
                            DEFAULT_ARGS_HANDLER.substitute(service=self.__service))
                    with open(self.__prop_file_path + self.__service + '-properties.conf', 'wb') as configfile:
                        cfg.write(configfile)
                except Exception, e:
                    file_logger.debug('Error in parsing file! Please validate the config file.')

    def change_severity_level(self):
        module_type = is_python_or_cpp(self.__service)
        cfg = ConfigParser.RawConfigParser()
        try:
            cfg.read(self.__conf_file_path + self.__service + '.conf')
            if module_type == 'c':
                cfg.set('DEFAULT', 'log_level', self.__log_severity_level)
            else:
                cfg.set('DEFAULTS', 'log_level', self.__log_severity_level)
            with open(self.__conf_file_path + self.__service + '.conf', 'wb') as configfile:
                cfg.write(configfile)
        except Exception, e:
            file_logger.debug('Error in parsing file! Please validate the config file.')


	 
