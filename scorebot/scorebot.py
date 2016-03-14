from random import randint
import logging
import board
import sb_logic
from pprint import pprint


class ScoreBot:

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

        # testb = [0, 1, 1, 0, 1, 2, 0, 2, 1]

        # logging.info("testb?!\n{}".format(pprint(testb)))
        # logging.info("test1?! {}".format(sb_logic.can_score(testb, 1)))
        # logging.info("test2?! {}".format(sb_logic.can_score(testb, 2)))
        # exit(-1)


        logging.info("winmat {}".format(board.winmatrix()))
        csm = board.canscorematrix()
        logging.info("canscoremat {}".format(csm))

        values = self.set_values(board)
        logging.info("values {}".format(values))

        best_moves = [k for k,v in values.iteritems() if v == max(values.values())]


        logging.info("best moves {}".format(best_moves))

        if len(best_moves) < 1:
            logging.error("There is no legal moves")
            for y in range(9):
                for x in range(9):
                    if board.field[y*9+x] == 0:
                        return (x, y)


        rm = randint(0, len(best_moves)-1)
        logging.info("rm {}".format(rm))
        return board.locs_to_move(*best_moves[rm])

    def set_values(self, board):

        values = {(b,l): 0.0 for b in range(9) for l in range(9)}

        win_value = 2000.0
        lose_board_value = -15.0
        score_value = 18.0
        bad_score_value = -12.0
        free_play_value = -8.0

        center_board_value = 0.5

        #priotize the center
        for i in range(9):
            values[(4,i)] += center_board_value

        # priortize the board that could cause us to win
        masked_macrob = [0 if i < 0 else i for i in board.macroboard]
        canwin = sb_logic.can_score(masked_macrob, self.myid)
        if canwin is not False:
            logging.info("CAN WIN BOARD {}".format(canwin))
            for l in range(9):
                values[canwin,l] += win_value
        # depriortize the board that could cause us to win
        canlose = sb_logic.can_score(masked_macrob, self.oppid)
        if canlose is not False:
            for b in range(9):
                values[b,canlose] += lose_board_value



        # priortize scoring
        csm = board.canscorematrix()
        for b in range(9):
            if csm[self.myid][b] is not False:
                values[b,csm[self.myid][b]] += score_value

        # depriortize him scoring
        for b in range(9):
            if csm[self.oppid][b] is not False:
                for b2 in range(9):
                    values[b2,b] += bad_score_value

        # don't give him free play
        for b in range(9):
            if board.macroboard[b] > 0:
                for b2 in range(9):
                    values[b2,b] += free_play_value

        legal_values = {k:v for k,v in values.iteritems() if k in board.legal_moves()}
        return legal_values
