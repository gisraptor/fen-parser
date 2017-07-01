# -*- coding: utf-8 -*-
"""This is the FEN notation parsing module."""
import re

class Position(object):
    """A FEN position as parsed from the FEN argument string

    >>> p = Position('rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1')
    """
    def __init__(self, fen):
        """Initialize a Position instance from a FEN string"""
        castle_validator = re.compile('^[KQkq-]+$')
        en_passant_validator = re.compile('^[a-h1-8-]+$')
        self.board = None
        self.active = None
        self.castle = None
        self.en_passant = None
        self.halfmove_clock = None
        self.fullmove_number = None
        self.fen = fen
        if not fen or not isinstance(fen, str):
            raise ValueError('FEN must be a string with six space-delimited fields')
        (placement, active, castle, en_passant,
                halfmove_clock, fullmove_number) = self.fen.split(' ')
        self.board = self.__build_board(placement)
        if active in ('w', 'b'):
            self.active = active
        else:
            raise ValueError('Invalid active color: %s' % active)
        if castle_validator.match(castle):
            self.castle = castle
        else:
            raise ValueError('Invalid castling availability: %s' % castle)
        if en_passant_validator.match(en_passant):
            self.en_passant = en_passant
        else:
            raise ValueError('Invalid en passant target: %s' % en_passant)
        if halfmove_clock.isdigit():
            self.halfmove_clock = halfmove_clock
        else:
            raise ValueError('The half move clock is not an integer: %s' % halfmove_clock)
        if fullmove_number.isdigit():
            self.fullmove_number = fullmove_number
        else:
            raise ValueError('The full move number is not an integer: %s' % fullmove_number)


    @staticmethod
    def __build_board(placement):
        """Expand a FEN placement string to replace integers with spaces"""
        validator = re.compile('^[RrNnBbQqKkPp1-8/]+$')
        match = validator.match(placement)
        if match:
            expander = {
                '1': ' ',
                '2': ' ' * 2,
                '3': ' ' * 3,
                '4': ' ' * 4,
                '5': ' ' * 5,
                '6': ' ' * 6,
                '7': ' ' * 7,
                '8': ' ' * 8,
            }
            expansion = ''.join(map(lambda ch: expander.get(ch, ch), placement))
            return expansion.split('/')
        else:
            raise ValueError('Invalid FEN placement string: %s' % placement)




if __name__ == "__main__":
    initial_fen = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'
    p = Position(initial_fen)
