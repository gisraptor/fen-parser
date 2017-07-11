# -*- coding: utf-8 -*-
"""
Tests for next-state FEN creation bases on a provided move
"""
import pytest
from fen import Position

@pytest.fixture
def samples():
    fen_move_samples = [
        ('rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1', 'a2a3',
         'rnbqkbnr/pppppppp/8/8/8/P7/1PPPPPPP/RNBQKBNR b KQkq - 0 1'),
        ('rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R b KQkq - 1 2', 'a7a5',
         'rnbqkbnr/1p1ppppp/8/p1p5/4P3/5N2/PPPP1PPP/RNBQKB1R w KQkq a6 0 3'),
        ('8/4npk1/5p1p/1Q5P/1p4P1/4r3/7q/3K1R2 b - - 1 49', 'b4b3',
         '8/4npk1/5p1p/1Q5P/6P1/1p2r3/7q/3K1R2 w - - 0 50'),
        ('5r1k/6pp/4Qpb1/p7/8/6PP/P4PK1/3q4 b - - 4 37', 'a5a4',
         '5r1k/6pp/4Qpb1/8/p7/6PP/P4PK1/3q4 w - - 0 38'),
        ('8/8/2P5/4B3/1Q6/4K3/6P1/3k4 w - - 5 67', 'b4a3',
         '8/8/2P5/4B3/8/Q3K3/6P1/3k4 b - - 6 67'),
        ('r2q1rk1/pp2ppbp/2p2np1/6B1/3PP1b1/Q1P2N2/P4PPP/3RKB1R b K - 0 13', 'a7a5',
         'r2q1rk1/1p2ppbp/2p2np1/p5B1/3PP1b1/Q1P2N2/P4PPP/3RKB1R w K a6 0 14'),
    ]
    fen_move_error_samples = [
        ('rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1', 'a7a6',
         'rnbqkbnr/1ppppppp/p7/8/8/8/PPPPPPPP/RNBQKBNR b KQkq - 0 1'),
        ('rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR b KQkq - 0 1', 'a2a3',
         'rnbqkbnr/pppppppp/8/8/8/P7/1PPPPPPP/RNBQKBNR w KQkq - 0 1'),
    ]
    fen_capture_error_samples = [
        ('rnbqkbnr/pppp2pp/5p2/4p3/4P3/3P4/PPP2PPP/RNBQKBNR w - - 0 1', 'd3e4',
         'rnbqkbnr/pppp2pp/5p2/4p3/4P3/8/PPP2PPP/RNBQKBNR w - - 0 1'),
    ]
    fen_capture_samples = [
        ('r1bqkb1r/pppp1ppp/2n2n2/4p3/3PP3/5N2/PPP2PPP/RNBQKB1R w KQkq - 1 4', 'd4e5',
         'r1bqkb1r/pppp1ppp/2n2n2/4P3/4P3/5N2/PPP2PPP/RNBQKB1R b KQkq - 0 4', 'p'),
        ('r1bqkb1r/pppp1ppp/2n2n2/4P3/4P3/5N2/PPP2PPP/RNBQKB1R b KQkq - 0 4', 'f6e4',
         'r1bqkb1r/pppp1ppp/2n5/4P3/4n3/5N2/PPP2PPP/RNBQKB1R w KQkq - 0 5', 'P'),
    ]
    fen_en_passant_samples = [
        ('rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1', 'e2e4',
         'rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq e3 0 1'),
        ('rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R b KQkq - 1 2', 'a7a5',
         'rnbqkbnr/1p1ppppp/8/p1p5/4P3/5N2/PPPP1PPP/RNBQKB1R w KQkq a6 0 3'),
    ]
    fen_halfmove_clock_reset_samples = [
        ('5r1k/6pp/4Qpb1/p7/8/6PP/P4PK1/3q4 b - - 4 37', 'a5a4',
         '5r1k/6pp/4Qpb1/8/p7/6PP/P4PK1/3q4 w - - 0 38'),
    ]
    fen_castling_samples = [
        ('r1bqkb1r/1p4pp/p1n1p3/3n1p2/3P4/2N2N2/PP2BPPP/R1BQK2R w KQkq - 2 11', 'e1g1',
         'r1bqkb1r/1p4pp/p1n1p3/3n1p2/3P4/2N2N2/PP2BPPP/R1BQ1RK1 b kq - 3 11'),
        ('r1b1k2r/1pq3pp/2n1p3/pB1P1p2/3N4/2P5/P4PPP/1R1QR1K1 b kq - 2 20', 'e8g8',
         'r1b2rk1/1pq3pp/2n1p3/pB1P1p2/3N4/2P5/P4PPP/1R1QR1K1 w - - 3 21'),
        ('r1b1k2r/1pq3pp/2n1p3/pB1P1p2/3N4/2P5/P4PPP/1R1QR1K1 b kq - 2 20', 'e8f7',
         'r1b4r/1pq2kpp/2n1p3/pB1P1p2/3N4/2P5/P4PPP/1R1QR1K1 w - - 3 21'),
    ]
    return {
        'moves': fen_move_samples,
        'invalid_piece_moves': fen_move_error_samples,
        'invalid_capture_moves': fen_capture_error_samples,      
        'capture_moves': fen_capture_samples,
        'en_passant_moves': fen_en_passant_samples,
        'halfmove_clock_reset_moves': fen_halfmove_clock_reset_samples,
        'castling_moves': fen_castling_samples,
    }


def test_move_only_moves_pieces_of_correct_color(samples):
    for sample in samples['invalid_piece_moves']:
        p = Position(sample[0])
        with pytest.raises(ValueError) as excinfo:
            actual = p.move_piece(sample[1])


def test_capture_only_pieces_of_correct_color(samples):
    for sample in samples['invalid_capture_moves']:
        p = Position(sample[0])
        with pytest.raises(ValueError) as excinfo:
            actual = p.move_piece(sample[1])


def test_move_calculates_en_passant(samples):
    for sample in samples['en_passant_moves']:
        p = Position(sample[0])
        actual = p.move_piece(sample[1])
        assert actual.fen == (sample[2])
        assert actual.en_passant != '-'


def test_fullmove_number_increments_on_black_turn_completion(samples):
    for sample in samples['moves']:
        p = Position(sample[0])
        actual = p.move_piece(sample[1])
        if p.active == 'b':
            expected_fullmove_number = p.fullmove_number + 1
        else:
            expected_fullmove_number = p.fullmove_number
        assert actual.fullmove_number == expected_fullmove_number


def test_halfmove_clock_resets_on_pawn_move(samples):
    for sample in samples['moves']:
        p = Position(sample[0])
        actual = p.move_piece(sample[1])
        if actual.piece_moved in 'Pp':
            assert actual.halfmove_clock == 0
    

def test_halfmove_clock_resets_on_capture(samples):
    for sample in samples['capture_moves']:
        p = Position(sample[0])
        actual = p.move_piece(sample[1])
        assert actual.halfmove_clock == 0


def test_halfmove_clock_increments_on_appropriate_moves(samples):
    for sample in samples['moves']:
        p = Position(sample[0])
        actual = p.move_piece(sample[1])
        if not actual.capture and actual.piece_moved not in 'Pp':
            assert int(actual.halfmove_clock) == int(p.halfmove_clock) + 1


def test_capture_set_on_appropriate_moves(samples):
    for sample in samples['capture_moves']:
        p = Position(sample[0])
        actual = p.move_piece(sample[1])
        assert actual.capture
        assert actual.fen == sample[2]
        assert actual.piece_captured == sample[3]


def test_castling_updates_on_castle(samples):
    for sample in samples['castling_moves']:
        p = Position(sample[0])
        actual = p.move_piece(sample[1])
        assert actual.fen == sample[2]


def test_move_piece_outputs_correct_fen(samples):
    for sample in samples['moves']:
        p = Position(sample[0])
        actual = p.move_piece(sample[1])
        assert actual.fen == sample[2]



