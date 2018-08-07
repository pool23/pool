"""
Purpose     : Extract data from comparefirst
        #####################     Change log   ###############################
        ##------------------------------------------------------------------##
        ##  Author              ##Date                ##Current Version     ##
        ##------------------------------------------------------------------##
        ## Moody's Analytics    ##11th July, 2018     ##V1.0                ##
        ##------------------------------------------------------------------##
        ######################################################################
        Date              Version     Author      Description
        11th July, 2018   v 1.0       Sairam      Data Extraction
"""
import inspect
import logging
import datetime
now = datetime.datetime.now()

file_name = 'log_file_'+now.strftime("%d-%m-%Y")+'.log'
def write_doc(doc=None):
    if doc is not None:
        with open(file_name,mode= 'a') as ftr:
            ftr.write(doc+"\n\n")

def function_logger(file_level, console_level = None):

    function_name = inspect.stack()[1][3]
    logger = logging.getLogger(function_name)
    logger.setLevel(logging.DEBUG) #By default, logs all messages

    if console_level != None:
        ch = logging.StreamHandler() #StreamHandler logs to console
        ch.setLevel(console_level)
        ch_format = logging.Formatter('%(asctime)s - %(message)s')
        ch.setFormatter(ch_format)
        logger.addHandler(ch)

    fh = logging.FileHandler(file_name)
    fh.setLevel(file_level)

    fh_format = logging.Formatter('%(asctime)s - %(lineno)d - %(levelname)-8s  - %(message)s')
    fh.setFormatter(fh_format)
    logger.addHandler(fh)

    return logger



# def f1():
#     f1_logger = function_logger(logging.DEBUG, logging.ERROR)
#     # f1_logger.write(dco__doc__)
#     f1_logger.info('info message')
#     f1_logger.warn('warn message')
#     f1_logger.error('error message')
#     f1_logger.critical('critical message')
#
# def f2():
#     f2_logger = function_logger(logging.WARNING)
#     f2_logger.debug('debug message')
#     f2_logger.info('info message')
#     f2_logger.warn('warn message')
#     f2_logger.error('error message')
#     f2_logger.critical('critical message')
#
# def main():
#     f1()
#     f2()
#     logging.shutdown()
# write_doc(doc =__doc__)
# main()