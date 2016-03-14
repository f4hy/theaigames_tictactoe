from random import randint
import logging
import board
import sb_logic
from pprint import pprint, pprint_field


class FirstBot:

    def __init__(self):
        self.currentboard = board.Board()
        self.nmove = 0

    def update_currentboard(self, fstring):
        logging.info("updating board")
        self.currentboard.setboard(fstring)

    def update_macroboard(self, mbstr):
        logging.info("setting macro board")
        self.currentboard.updatemacroboard(mbstr)

    def set_movenumb(self, nmove):
        logging.info("N move set to {}".format(nmove))
        self.nmove = nmove

    def myid(self, myid):
        self.myid = myid
        if myid == 2:
            self.oppid = 1
        else:
            self.oppid = 2

    def make_move(self, time):
        return self.best_move(self.currentboard, time)

    def best_move(self, board, tleft):
        logging.info("get_move {} {}".format(board, tleft))

        logging.info("winmat {}".format(board.winmatrix()))
        csm = board.canscorematrix()
        logging.info("canscoremat {}".format(csm))

        for sbi in range(9):
            if board.macroboard[sbi] == -1 and csm[self.myid][sbi]:
                scoring_loc = csm[self.myid][sbi]
                logging.info("we can score on board {} loc {}".format(sbi, scoring_loc))
                scoring_move = board.locs_to_move(sbi, scoring_loc)
                logging.info("we can score with move {}".format(scoring_move))
                logging.info("sb\n{}".format(pprint(board.get_subboard(sbi))))
                logging.info("canscore \n{}".format(sb_logic.can_score(board.get_subboard(sbi), self.myid)))
                return scoring_move

        # logging.info("board {}".format(board.get_board()))
        lmoves = board.legal_moves()
        logging.info("lmoves {}".format(lmoves))

        rm = randint(0, len(lmoves)-1)
        logging.info("rm {}".format(rm))
        return board.locs_to_move(*lmoves[rm])
