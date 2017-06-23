from time import gmtime, strftime

class Log:
    def __init__(self, _message):
        f = file('log/'+strftime("%Y-%m-%d %H", gmtime())+'.log', 'a')

        text =strftime("%Y-%m-%d %H:%M:%S", gmtime())+' - '+_message+'\n'

        print text
        f.writelines(text)

        f.flush()
        f.close()
