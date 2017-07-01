# -*- coding: utf-8 -*-
"""
Tests for board display engine
"""
import pytest
from fen import Position
from display import render_ascii_board

@pytest.fixture
def samples():
    board_samples = [
        [
            'rnbqkbnr',
            'pppppppp',
            '        ',
            '        ',
            '        ',
            '        ',
            'PPPPPPPP',
            'RNBQKBNR',
        ]
    ]
    expected_output = {
        'ascii':
"""  ---------------------------------
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
    a   b   c   d   e   f   g   h
"""
    }
    return { 'boards': board_samples, 'output': expected_output }


def test_ascii_display(samples):
    assert render_ascii_board(samples['boards'][0]) == samples['output']['ascii']
