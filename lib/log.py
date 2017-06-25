# -*- coding: utf-8 -*-
"""
Log module a simple class to save ProxY log in text files, located
in log diretory.
"""
from time import gmtime, strftime

__docformat__ = 'reStructuredText'


class Log:
    '''
    writes **_message** in log file.
    
    :param _message: the log entry
    '''
    def __init__(self, _message):

        f = file('log/'+strftime("%Y-%m-%d %H", gmtime())+'.log', 'a')

        text =strftime("%Y-%m-%d %H:%M:%S", gmtime())+' - '+_message+'\n'

        print text
        f.writelines(text)

        f.flush()
        f.close()
