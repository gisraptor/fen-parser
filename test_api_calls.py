# -*- coding: utf-8 -*-
"""
Tests for Syzygy endgame tablebases API
"""
import sys
import pytest
from syzygymoves import parse_args, main

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
    argument_test_samples = [
        [['8/4npk1/5p1p/1Q5P/1p4P1/4r3/7q/3K1R2 b - - 1 49', '-vvvv'],
         {'fen': '8/4npk1/5p1p/1Q5P/1p4P1/4r3/7q/3K1R2 b - - 1 49', 'verbosity': 0}],
        [['r2q1rk1/pp2ppbp/2p2np1/6B1/3PP1b1/Q1P2N2/P4PPP/3RKB1R b K - 0 13', '-q'],
         {'fen': 'r2q1rk1/pp2ppbp/2p2np1/6B1/3PP1b1/Q1P2N2/P4PPP/3RKB1R b K - 0 13', 'quiet': True}],
        [['8/8/2P5/4B3/1Q6/4K3/6P1/3k4 w - - 5 67', '--log-file=chess.log'],
         {'fen': '8/8/2P5/4B3/1Q6/4K3/6P1/3k4 w - - 5 67', 'log_file': 'chess.log'}],
        [[],
         {'fen': 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'}],
    ]
    return { 'valid': fen_move_samples , 'arguments': argument_test_samples }


def test_argument_parser(samples):
    for argument_test_set in samples['arguments']:
        sys.argv = ['',] + argument_test_set[0]
        args = parse_args()
        assert args.fen == argument_test_set[1].get('fen', 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1')
        assert args.verbose == argument_test_set[1].get('verbosity', 30)
        assert args.quiet == argument_test_set[1].get('quiet', False)
        assert args.log_file == argument_test_set[1].get('log_file', None)


# Not quite sure how to effectively test this without refactoring the main method.
# The function below tests that no exceptions are thrown by the calls to main, but
# it is not an effective test.
def test_api_call(samples):
    for move in samples['valid']:
        sys.argv = ['',] + [move[0]]
        args = parse_args()
        main(args)

