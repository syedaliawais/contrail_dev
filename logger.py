import logging
import sys
from config import *
#
# Main implementation of Logger class
#
class Logger():
    #
    # Constructor implementation
    # This will get the logger file and handler instantiated.
    # It is very basic config. We can expand on it if need be.
    #
    def __init__(self, module_name):
        try:
            file_name = "%s/%s.log" % (DIR_PATH, module_name)
            logging.basicConfig(filename=file_name, level=logging.DEBUG,
                                format='%(asctime)s %(message)s')
            self.logger = logging.getLogger(module_name)
        except:
            print "Unable to instantiate logger:", sys.exc_info()[0]
            raise

    #
    # This function when called, will return logger with an extra handler
    # for handling console output. Useful for debugging on console.
    #
    def get_logger_with_console(self):
        ch = logging.StreamHandler()
        self.logger.addHandler(ch)
        return self.logger

    #
    # Get the logger object
    #
    def get_logger(self):
        return self.logger