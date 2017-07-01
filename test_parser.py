# -*- coding: utf-8 -*-
"""
Tests for FEN parsing
"""
import re
import pytest
from fen import Position

@pytest.fixture
def samples():
    valid_fen_samples = [
        'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1',
        'rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq e3 0 1',
        'rnbqkbnr/ppp1pppp/8/3p4/4P3/8/PPPP1PPP/RNBQKBNR w KQkq d6 0 2',
        'rnbqkbnr/ppp1pppp/8/3P4/8/8/PPPP1PPP/RNBQKBNR b KQkq - 0 2',
        'rnb1kbnr/ppp1pppp/8/3q4/8/8/PPPP1PPP/RNBQKBNR w KQkq - 0 3',
        'rnb1kbnr/ppp1pppp/8/3q4/3P4/8/PPP2PPP/RNBQKBNR b KQkq d3 0 3',
        'rnb1kbnr/ppp2ppp/8/3qp3/3P4/8/PPP2PPP/RNBQKBNR w KQkq e6 0 4',
        'rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R b KQkq - 1 2',
        '8/4npk1/5p1p/1Q5P/1p4P1/4r3/7q/3K1R2 b - - 1 49',
        '5r1k/6pp/4Qpb1/p7/8/6PP/P4PK1/3q4 b - - 4 37',
        '8/8/2P5/4B3/1Q6/4K3/6P1/3k4 w - - 5 67',
        'r2q1rk1/pp2ppbp/2p2np1/6B1/3PP1b1/Q1P2N2/P4PPP/3RKB1R b K - 0 13',
        'r1b1k1nr/ppp2ppp/2n5/3qp1N1/1b1P4/P1N1B3/1PP2PPP/R2QKB1R b KQkq - 0 10',
    ]
    invalid_fen_samples = [
        'rnbqkbnr/ppppptpp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1',
        'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR n KQkq - 0 1',
        'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w 0 - 0 1',
        'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq x 0 1',
        'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - a 1',
        'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 N',
        'htrpqqnk4/2093jd/alk2j3hh|\\98308sjaqwlkjASJKW/ajskkeh',
        '',
        None,
        object()
    ]
    return { 'valid': valid_fen_samples, 'invalid': invalid_fen_samples }


def test_invalid_fen_raise_error(samples):
    for sample in samples['invalid']:
        with pytest.raises(ValueError) as excinfo:
            p = Position(sample)


def test_six_space_separated_fields(samples):
    for sample in samples['valid']:
        p = Position(sample)
        assert p.board != None
        assert p.active != None
        assert p.castle != None
        assert p.en_passant != None
        assert p.halfmove_clock != None
        assert p.fullmove_number != None


def test_active_color(samples):
    for sample in samples['valid']:
        p = Position(sample)
        assert p.active in ('w', 'b')


def test_castle_values(samples):
    castle_verifier = re.compile('^[KQkq-]+$')
    for sample in samples['valid']:
        p = Position(sample)
        assert castle_verifier.match(p.castle)


def test_en_passant_values(samples):
    en_passant_verifier = re.compile('^[a-h1-8-]+$')
    for sample in samples['valid']:
        p = Position(sample)
        assert en_passant_verifier.match(p.en_passant)


def test_halfmove_clock(samples):
    for sample in samples['valid']:
        p = Position(sample)
        assert p.halfmove_clock.isdigit()


def test_fullmove_number(samples):
    for sample in samples['valid']:
        p = Position(sample)
        assert p.fullmove_number.isdigit()
