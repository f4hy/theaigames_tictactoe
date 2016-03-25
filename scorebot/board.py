import logging
import sb_logic
from pprint import pprint, pprint_field


class Board(object):

    def __init__(self):
        self.field = [[0 for i in range(9)] for j in range(9)]
        self.macroboard = None

    def setboard(self, fstr):
        flist = fstr.replace(';', ',').split(',')
        logging.info(flist)
        self.field = [ int(f) for f in flist]
        logging.info("field {}".format(self.field))
        logging.info("board \n{}".format(pprint_field(self.field)))
        logging.info("sb0 board \n{}".format(pprint(self.get_subboard(0))))
        logging.info("sb8 board \n{}".format(pprint(self.get_subboard(8))))


    def is_legal(self, b, loc):
        return self.macroboard[b] == -1 and self.get_subboard(b)[loc] == 0


    def legal_moves(self):
        return [ (b, loc) for b in range(9) for loc in range(9) if self.is_legal(b, loc) ]


    def updatemacroboard(self, mbstr):
        mblist = mbstr.replace(';', ',').split(',')
        self.macroboard = [ int(f) for f in mblist]
        logging.info("mboard \n{}".format(pprint(self.macroboard)))

    def get_subboard(self, index):
        mx = index % 3
        my = index//3
        sb = [self.field[(y)*9+(x)] for y in range(my*3, my*3+3) for x in range(mx*3, mx*3+3)]
        return sb

    def get_all_subs(self):
        sbs = [self.get_subboard(i) for i in range(9)]
        return sbs

    def winmatrix(self):
        m = {}
        for t in (1, 2):
            m[t] = [sb_logic.won(sb, t) for sb in self.get_all_subs()]

        return m

    def canscorematrix(self):
        m = {}
        for t in (1, 2):
            m[t] = [sb_logic.can_score(sb, t) for sb in self.get_all_subs()]
        return m

    def catsmatrix(self):
        m = [sb_logic.cats(sb) for sb in self.get_all_subs()]
        return m


    def playable_subs(self):
        allsubs = self.get_all_subs()
        return [allsubs[i] for i in range(9) if self.macroboard[i] == -1]

    def locs_to_move(self, b, s):
        """ take a board index and square index and make a move"""
        mx = b % 3
        my = b//3
        x = s % 3
        y = s//3
        return (mx*3+x, my*3+y)
