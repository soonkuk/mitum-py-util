LOG_SHA256 = 'sha256'
LOG_BCONCAT = 'bconcat'
LOG_TO_BYTES = 'to_bytes'

def clog(caller, func, msg):
    if func == LOG_SHA256:
        print('[CALL] ' + func + '(' + str(msg) + ')')
        return
    elif func == LOG_BCONCAT:
        print('[CALL] ' + func + ': '+ str(msg))
    elif func == LOG_TO_BYTES:
        print('[CALL] ' + caller + '.' + func + '()')
    

def rlog(caller, func, msg, *result):
    clog(caller, func, msg)
    for r in result:
        print('-', r)
    print()