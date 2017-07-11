# -*- coding: utf-8 -*-
"""This is the FEN notation parsing module."""
import copy
import re
from display import render_ascii_board

class Position(object):
    """A FEN position as parsed from the FEN argument string

    >>> p = Position('rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1')
    >>> print(p)
      ---------------------------------
    8 | r | n | b | q | k | b | n | r |
      |-------------------------------|
    7 | p | p | p | p | p | p | p | p |
      |-------------------------------|
    6 |   |   |   |   |   |   |   |   |
      |-------------------------------|
    5 |   |   |   |   |   |   |   |   |
      |-------------------------------|
    4 |   |   |   |   |   |   |   |   |
      |-------------------------------|
    3 |   |   |   |   |   |   |   |   |
      |-------------------------------|
    2 | P | P | P | P | P | P | P | P |
      |-------------------------------|
    1 | R | N | B | Q | K | B | N | R |
      ---------------------------------
    """
    rank_translation = {
        'a': 0,
        'b': 1,
        'c': 2,
        'd': 3,
        'e': 4,
        'f': 5,
        'g': 6,
        'h': 7,
    }
    algebraic_translation = {
        0: 'a',
        1: 'b',
        2: 'c',
        3: 'd',
        4: 'e',
        5: 'f',
        6: 'g',
        7: 'h',
    }

    def __init__(self, fen, renderer=render_ascii_board):
        """Initialize a Position instance from a FEN string"""
        castle_validator = re.compile('^[KQkq-]+$')
        en_passant_validator = re.compile('^[a-h1-8-]+$')
        self.board = None
        self.active = None
        self.castling_availability = None
        self.en_passant = None
        self.halfmove_clock = None
        self.fullmove_number = None
        self.fen = fen
        if not fen or not isinstance(fen, str):
            raise ValueError('FEN must be a string with six space-delimited fields')
        (placement, active, castling_availability, en_passant,
                halfmove_clock, fullmove_number) = self.fen.split(' ')
        self.board = self.__build_board(placement)
        if active in ('w', 'b'):
            self.active = active
        else:
            raise ValueError('Invalid active color: %s' % active)
        if castle_validator.match(castling_availability):
            self.castling_availability = castling_availability
        else:
            raise ValueError('Invalid castling availability: %s' % castling_availability)
        if en_passant_validator.match(en_passant):
            self.en_passant = en_passant
        else:
            raise ValueError('Invalid en passant target: %s' % en_passant)
        if halfmove_clock.isdigit():
            self.halfmove_clock = int(halfmove_clock)
        else:
            raise ValueError('The half move clock is not an integer: %s' % halfmove_clock)
        if fullmove_number.isdigit():
            self.fullmove_number = int(fullmove_number)
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


    def __str__(self):
        return render_ascii_board(self.board)


    def move_piece(self, move):
        new_position = copy.deepcopy(self)
        new_position._current_rank = self.rank_translation.get(move[0])
        new_position._current_file = 8 - int(move[1])
        new_position._new_rank = self.rank_translation.get(move[2])
        new_position._new_file = 8 - int(move[3])
        new_position._Position__set_piece_moved()
        new_position._Position__set_capture()
        new_position._Position__set_en_passant()
        new_position._Position__set_castling()
        new_position._Position__set_active()
        new_position._Position__set_fullmove_number()
        new_position._Position__set_halfmove_clock()
        new_position._Position__execute_move()
        new_position._Position__construct_updated_fen()
        return new_position


    def __set_piece_moved(self):
        #print(self)
        #print("rank: %r" % self._current_rank)
        #print("file: %r" % self._current_file)
        self.piece_moved = self.board[self._current_file][self._current_rank]
        #print("piece_moved: %r" % self.piece_moved)
        if self.active == 'w' and not self.piece_moved.isupper() or self.active == 'b' and not self.piece_moved.islower():
            raise ValueError('The piece being moved is not the correct color.')


    def __set_capture(self):
        #print(self)
        #print("current rank: %r" % self._current_rank)
        #print("current file: %r" % self._current_file)
        #print("new rank: %r" % self._new_rank)
        #print("new file: %r" % self._new_file)
        self.piece_captured = self.board[self._new_file][self._new_rank]
        self.capture = self.piece_captured != ' '
        #print("capture: %r" % self.capture)
        if self.active == 'w' and self.piece_captured.isupper() or self.active == 'b' and self.piece_captured.islower():
            raise ValueError('The piece being captured is not the correct color.')


    def __set_en_passant(self):
        #print("current rank: %r" % self._current_rank)
        #print("current file: %r" % self._current_file)
        #print("new rank: %r" % self._new_rank)
        #print("new file: %r" % self._new_file)
        #print("active: %r" % self.active)
        if self.piece_moved in 'Pp':
            if self.active == 'w' and self._current_file - self._new_file == 2 and self._new_rank == self._current_rank:
                self.en_passant = self.algebraic_translation.get(self._new_rank) + str(8 - (self._new_file + 1))
            elif self.active == 'b' and self._new_file - self._current_file == 2 and self._new_rank == self._current_rank:
                self.en_passant = self.algebraic_translation.get(self._new_rank) + str(8 - (self._new_file - 1))
        else:
            self.en_passant = '-'
        #print("en passant: %r" % self.en_passant)


    def __set_castling(self):
        if self.piece_moved in 'Kk':
            if self.piece_moved.isupper():
                self.castling_availability = re.sub('([KQ]+)', '', self.castling_availability)
            elif self.piece_moved.islower():
                self.castling_availability = re.sub('([kq]+)', '', self.castling_availability)
        elif self.piece_moved in 'Rr':
            if self.piece_moved.isupper():
                if self._current_rank == 0:
                    remove_exp = 'Q'
                elif self._current_rank == 8:
                    remove_exp = 'K'
            elif self.piece_moved_islower():
                if self._current_rank == 0:
                    remove_exp = 'q'
                elif self._current_rank == 8:
                    remove_exp = 'k'
            self.castling_availability.replace(remove_exp, '')
        if self.castling_availability == '':
            self.castling_availability = '-'


    def __set_active(self):
        if self.active == 'w':
            self.active = 'b'
        elif self.active == 'b':
            self.active = 'w'
        else:
            raise ValueError('Invalid active field value.')


    def __set_fullmove_number(self):
        if self.active == 'w':
            self.fullmove_number = self.fullmove_number + 1
        

    def __set_halfmove_clock(self):
        if self.piece_moved in 'Pp' or self.capture:
            #print('halfmove_clock 1: %r' % self.halfmove_clock)
            self.halfmove_clock = 0
            #print('halfmove_clock 2: %r' % self.halfmove_clock)
        else:
            #print('halfmove_clock 1: %r' % self.halfmove_clock)
            self.halfmove_clock += 1
            #print('halfmove_clock 2: %r' % self.halfmove_clock)


    def __execute_move(self, move=None):
        from_file = list(self.board[self._current_file])
        from_file[self._current_rank] = ' '
        self.board[self._current_file] = ''.join(from_file)
        to_file = list(self.board[self._new_file])
        to_file[self._new_rank] = self.piece_moved
        self.board[self._new_file] = ''.join(to_file)
        if self.piece_moved in 'Kk':
            # If the king moved 2 spaces then castling is taking place
            if abs(self._current_rank - self._new_rank) == 2:
                rook_file = list(self.board[self._current_file])
                if self._current_rank > self._new_rank:
                    rook_current_rank = 0
                    rook_new_rank = 3
                else:
                    rook_current_rank = 7
                    rook_new_rank = 5
                rook_file[rook_current_rank] = ' '
                rook_piece = 'R'
                if self.piece_moved.islower():
                    rook_piece = 'r'
                rook_file[rook_new_rank] = rook_piece
                self.board[self._current_file] = ''.join(rook_file)
        self.__construct_updated_fen()


    def __construct_updated_fen(self):
        template = "%s %s %s %s %i %i"
        board = '/'.join(self.board)
        board = re.sub('( +)', lambda matchobj: str(len(matchobj.group(0))), board)
        self.fen = template % (board, self.active, self.castling_availability, self.en_passant, self.halfmove_clock, self.fullmove_number)


if __name__ == "__main__":
    initial_fen = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'
    p = Position(initial_fen)
    print(p)
