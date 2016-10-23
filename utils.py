#!/bin/python
from config import *
import os.path
from logger import Logger
import ConfigParser

file_logger = Logger('log-manager').get_logger_with_console()


def is_python_or_cpp(module_name):
    for key, value in MODULE_DICT.iteritems():
        for val in value:
            if module_name == val:
                return key


def conv_service_name_from_hyphen_to_underscore(service_name):
    return '_'.join(s for s in service_name.split('-'))


def write_template_to_file(prop_path, module_name, module_type, string):
    if module_type == 'p':
        with open(prop_path + module_name + '-properties.conf', 'w') as conf_file:
            conf_file.write(string)
    else:
        with open(prop_path + module_name + '-properties.properties', 'w') as prop_file:
            prop_file.write(string)


def write_value_to_property_file(prop_path, module_name, value):
    lines = ''
    with open(prop_path + module_name + "-properties.properties", "r") as f:
        lines = f.readlines()
        for i, line in enumerate(lines):
            if line.startswith('log4cplus.appender.logfile.layout.ConversionPattern'):
                line_splitter = line.split('=')
                line_splitter[1] = value
                lines[i] = ('=').join(l for l in line_splitter)

    with open(prop_path + module_name + "-properties.properties", "w") as f:
        f.write(('\n').join(lines))


def write_value_to_config_file(prop_path, module_name, section, key, value):
    cfg = ConfigParser.RawConfigParser()
    cfg.read(prop_path + module_name + '-properties.conf')
    try:
        cfg.set(section, key, value)
        with open(prop_path + module_name + '-properties.conf', 'wb') as configfile:
            cfg.write(configfile)
    except Exception, e:
        file_logger.debug('Error in setting value: %s', e)


def log_format_formatter(str_format, module_type):
    str_splitted = str_format.split(',')
    formatted = ''
    for flag in str_splitted:
        if flag in COMMON_FORMAT_FLAGS_DICT:
            formatted += COMMON_FORMAT_FLAGS_DICT[flag][module_type] + ' '

    return formatted


def property_file_exists(prop_path, module_name, module_type):
    try:
        if module_type == 'p':
            return os.path.isfile(prop_path + module_name + '-properties' + '.conf')
        else:
            return os.path.isfile(prop_path + module_name + '-properties' + '.properties')
    except IOException, e:
        file_logger.debug('File not found...%s', e)
        return False
      
