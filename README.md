# contrail_dev
 Utility for enhancing the Contrail Logging functionality and adding flexibility in defining Logging patterns and formats along with severity levels

# Using the Utility

python contrail-manage-logs.py -h
```
usage: contrail-manage-logs.py  [-h] 
								-s SERVICE_NAME 
								[-d DISABLE_LOGS]
								[-log_level LOG_LEVEL] 
								[-pattern PATTERN]
								[-df DATE_FORMAT] 
								[-structured STRUCTURED_LOGS]
								-conf_file_path CONF_FILE_PATH
								-property_file_path PROPERTY_FILE_PATH
                               
Describes the utility usage

optional arguments:
  -h, --help            show this help message and exit
  -s SERVICE_NAME, --service_name SERVICE_NAME
                        
								contrail-api
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
								ifmap
								
  -d DISABLE_LOGS, --disable_logs DISABLE_LOGS
                 For disabling logs 1, for enabling 0
								 
  -log_level LOG_LEVEL, --log_level LOG_LEVEL
								 SYS_EMERG
								 SYS_ALERT
								 SYS_CRIT
								 SYS_ERR
								 SYS_WARN
								 SYS_NOTICE
								 SYS_INFO
								 SYS_DEBUG. Default is SYS_DEBUG
								 
  -pattern PATTERN, --pattern PATTERN
                 (asctime)s {(name)s}: (message)s
								 (name)s {(message)s}: (asctime)s
								 (asctime)s {(name)s}: (message)s :(thread)d
								 (asctime)s {(name)s}: (message)s :(thread)d : (processName)s
                                             
  -df DATE_FORMAT, --date_format DATE_FORMAT
                  Date Format of the Date in Logs i.e "m/d/Y I:M:S p" 
												
  -structured STRUCTURED_LOGS, --structured_logs STRUCTURED_LOGS
                  Structured Logs would change the logging format
												
  -conf_file_path CONF_FILE_PATH, --conf_file_path CONF_FILE_PATH
                  Path of the service config file i.e /etc/contrail/ 
												
  -property_file_path PROPERTY_FILE_PATH, --property_file_path PROPERTY_FILE_PATH
                  Path where the property file will be generated
