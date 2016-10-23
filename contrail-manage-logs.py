from argparse import RawTextHelpFormatter
import argparse
from logmanager import *


def get_args():
    parser = argparse.ArgumentParser(description='Describes the utility usage', formatter_class=RawTextHelpFormatter)
    parser.add_argument('-s', '--service_name', type=str,
                        help='''
                             contrail-api'
                             contrail-vrouter-agent
                             contrail-vrouter-nodemgr
                             contrail-control
                             contrail-control-nodemgr
                             contrail-dns
                             contrail-named
                             contrail-analytics-api
                             contrail-analytics-nodemgr
                             contrail-collector
                             contrail-query-engine
                             contrail-snmp-collector
                             contrail-topology
                             contrail-api:0
                             contrail-config-nodemgr
                             contrail-discovery:0
                             contrail-schema
                             contrail-svc-monitor
                             ifmap''', required=True)
    parser.add_argument('-d', '--disable_logs', type=int, help='For disabling logs 1, for enabling 0', required=False)
    parser.add_argument('-log_level', '--log_level', type=str,
                        help='''
                           SYS_EMERG
                           SYS_ALERT
                           SYS_CRIT
                           SYS_ERR
                           SYS_WARN
                           SYS_NOTICE
                           SYS_INFO
                           SYS_DEBUG. Default is SYS_DEBUG''')

    parser.add_argument('-pattern', '--pattern', type=str,
                        help='''
                     (asctime)s {(name)s}: (message)s
                     (name)s {(message)s}: (asctime)s
                     (asctime)s {(name)s}: (message)s :(thread)d
                     (asctime)s {(name)s}: (message)s :(thread)d : (processName)s
                     ''')
    parser.add_argument('-df', '--date_format', type=str, help='Date Format of the Date in Logs i.e "m/d/Y I:M:S p" ',
                        required=False)
    parser.add_argument('-structured', '--structured_logs', type=bool,
                        help='Structured Logs would change the logging format', required=False)
    parser.add_argument('-conf_file_path', '--conf_file_path', type=str,
                        help='Path of the service config file i.e /etc/contrail/ ', required=True)
    parser.add_argument('-property_file_path', '--property_file_path', type=str,
                        help='Path where the property file will be generated', required=True)
    args = parser.parse_args()
    service_name, disable_logs, pattern, date_format, structured, severity_level, conf_file_path, \
        property_file_path = args.service_name, args.disable_logs, args.pattern, args.date_format, args.structured_logs, \
                         args.log_level, args.conf_file_path, args.property_file_path
    return (
        service_name, disable_logs, pattern, date_format, structured, severity_level,
        conf_file_path, property_file_path)


def main():
    service_name, disable_logs, pattern, date_format, structured, severity_level, conf_file_path, \
        property_file_path = get_args()
    if authenticate_request():
        log_manager = LogManager(service_name, conf_file_path, property_file_path, structured, pattern, date_format,
                                 severity_level)
        module_type = is_python_or_cpp(service_name)
        if module_type == 'p':
            if pattern is not None:
                log_manager.change_python_logging_format()
        else:
            if pattern is not None:
                log_manager.change_cpp_logging_format()
        if disable_logs is not None:
            if disable_logs == 1:
                log_manager.disable_logs()
            else:
                log_manager.enable_logs()
        if severity_level is not None:
            log_manager.change_severity_level()
        if structured is not None:
            pass

if __name__ == '__main__':
    main()

