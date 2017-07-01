# -*- coding: utf-8 -*-
"""This is the display module to show a chess board"""

def render_ascii_board(matrix):
    end_line_template = '  ---------------------------------\n'
    intermediary_line_template = '  |-------------------------------|\n'
    file_template = '    a   b   c   d   e   f   g   h\n'
    rank_template = '%s | %s | %s | %s | %s | %s | %s | %s | %s |\n'
    board = end_line_template
    for index, rank in enumerate(matrix):
        board += rank_template % tuple(str(8 - index) + rank)
        if index < 7:
            board += intermediary_line_template
    board += end_line_template + file_template
    return board
