from random import randint
import logging

class RandomBot:

    def get_move(self, pos, tleft):
        logging.info("get_move {} {}".format(pos, tleft))
        #pos.parse_field()
        # logging.info("board {}".format(pos.get_board()))
        lmoves = pos.legal_moves()
        logging.info("lmoves {}".format(lmoves))
        rm = randint(0, len(lmoves)-1)
        logging.info("rm {}".format(rm))
        return lmoves[rm]
