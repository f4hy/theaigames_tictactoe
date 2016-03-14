#!/usr/bin/env python2


def parse_command(instr, bot):
    if instr.startswith('action move'):
        time = int(instr.split(' ')[-1])
        x, y = bot.make_move(time)
        return 'place_move %d %d\n' % (x, y)
    elif instr.startswith('update game field'):
        fstr = instr.split(' ')[-1]
        bot.update_currentboard(fstr)
    elif instr.startswith('update game macroboard'):
        mbstr = instr.split(' ')[-1]
        bot.update_macroboard(mbstr)
    elif instr.startswith('update game move'):
        bot.set_movenumb(int(instr.split(' ')[-1]))
    elif instr.startswith('settings your_botid'):
        myid = int(instr.split(' ')[-1])
        bot.myid(myid)
        bot.myid = myid
        bot.oppid = 1 if myid == 2 else 2
    elif instr.startswith('settings timebank'):
        bot.timebank = int(instr.split(' ')[-1])
    elif instr.startswith('settings time_per_move'):
        bot.time_per_move = int(instr.split(' ')[-1])
    return ''

if __name__ == '__main__':
    import sys
    from firstbot import FirstBot
    import logging
    import socket

    if 'f4hy' in socket.gethostname() or 'fahy' in socket.gethostname():
        logging.basicConfig(format='FIRSTBOT %(levelname)s: %(message)s', level=logging.DEBUG)
        root = logging.getLogger()
        errfilename = "test"+".err"
        errfilehandler = logging.FileHandler(errfilename, delay=True)
        errfilehandler.setLevel(logging.WARNING)
        formatter = logging.Formatter('FIRSTBOT %(levelname)s: %(message)s')
        errfilehandler.setFormatter(formatter)
        root.addHandler(errfilehandler)
        logfilename = "test"+".log"
        logfilehandler = logging.FileHandler(logfilename, delay=True)
        logfilehandler.setLevel(logging.DEBUG)
        formatter = logging.Formatter('FIRSTBOT %(levelname)s: %(message)s')
        logfilehandler.setFormatter(formatter)
        root.addHandler(logfilehandler)

    logging.info("starting logging")

    bot = FirstBot()

    while True:
        try:
            instr = raw_input()
            logging.info("instr {}".format(instr))
        except EOFError as e:
            logging.warn("given EOF exiting")
            sys.stdout.flush()
            exit(-1)
        except Exception as e:
            logging.warn('error reading input {}, {}'.format(e, type(e)))
            sys.stderr.write('error reading input')
            raise e
        outstr = parse_command(instr, bot)
        sys.stdout.write(outstr)
        sys.stdout.flush()
