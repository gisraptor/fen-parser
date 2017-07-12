# -*- coding: utf-8 -*-
"""
Script to call the chess move API at https://syzygy.info/api/v2

When provided a FEN string to start from this script will display the initial
position, call the API, choose the first move provided from the returned JSON,
generate the next FEN string and display the game board created by the given
move. If no FEN string is provided, the script will start with the default
initial position of the board.
"""
import argparse
from collections import OrderedDict
import datetime
import json
import logging
import logging.handlers
import os
import sys
import traceback

import requests
from fen import Position


def main(args):
    logger = logging.getLogger(__name__)

    start = datetime.datetime.now()

    # Do something cool in here
    try:
        logger.debug('args.fen: %r', args.fen)
        p1 = Position(args.fen)
        syzygy_params = { 'fen': p1.fen }
        response = requests.get('https://syzygy-tables.info/api/v2', params=syzygy_params)
        j = response.json(object_pairs_hook=OrderedDict)
        print(p1)
        moves = list(j['moves'].keys())
        print(moves)
        move = moves[0]
        p2 = p1.move_piece(move)
        print(p2)

    # Handle specific errors
    except ValueError:
        raise
    # Handle any unknown errors here
    except:
        tb = sys.exc_info()[2]
        tbinfo = traceback.format_tb(tb)[0]
        pymsg = 'PYTHON ERRORS:\nTraceback info:\n' + tbinfo + '\nError Info:\n' + str(sys.exc_info()[1])
        if tbinfo:
            logger.exception(pymsg + '\n')
        raise
    # Run this code no matter what happens with the errors
    finally:
        end = datetime.datetime.now()
        total = end - start
        days = total.days
        hours = divmod(total.seconds, 3600)
        minutes = divmod(hours[1], 60)
        seconds = minutes[1]
        logger.info('Processing took {0} days, {1} hours, {2} minutes and {3} seconds.'.format(days, hours[0], minutes[0], seconds))


def parse_args():
    """Parse the arguments entered by the user. Run syzygymoves.py --help for more information."""
    logger = logging.getLogger(__name__)

    class VerboseAction(argparse.Action):
        """Class to allow verbosity to build up.

        If the user specifies multiple -v arguments, then this class will count
        them and set the appropriate logging level."""
        verbosity_lookup = {
            0: logging.WARNING,
            1: logging.INFO,
            2: logging.DEBUG,
            3: logging.NOTSET,
        }
        verbosity = 0


        def __init__(self,
                     option_strings,
                     dest,
                     const,
                     default=None,
                     required=False,
                     help=None,
                     metavar=None):
            self.logger = logging.getLogger('parse_args.VerboseAction')
            super(VerboseAction, self).__init__(
                option_strings=option_strings,
                dest=dest,
                nargs=0,
                const=const,
                default=default,
                required=required,
                help=help
            )


        def __call__(self, parser, namespace, values, option_string=None):
            self.logger.debug('Parser: %r\nNamespace: %r\nDest: %r\nConst: %r\nValues: %r\nOption_string: %r\n' %
                (parser, namespace, self.dest, self.const, values, option_string)
            )
            self.verbosity += self.const
            setattr(namespace, self.dest,
                    self.verbosity_lookup.get(self.verbosity, logging.NOTSET)
            )


    logger.debug(sys.argv)
    parser = argparse.ArgumentParser(
        description='Find the next move for the given FEN and present the new FEN and board to the user.'
    )
    parser.add_argument('fen', metavar='FEN', type=str, action='store',
        default = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1',
        help='The FEN position string to start from', nargs='?')
    log_group = parser.add_argument_group('logging options')
    log_group.add_argument('-v', '--verbose', const=1, dest='verbose',
        default=logging.WARNING, action=VerboseAction,
        help='increase the amount of logging\n(may be added multiple times)'
    )
    log_group.add_argument('-q', '--quiet', help='prevent output to the console', action='store_true')
    log_group.add_argument('--log-file', help='the file to which log messages will be directed')
    parsed_args = parser.parse_args()
    logger.debug(parsed_args)
    return parsed_args


if __name__ == '__main__':
    # Initialize logging
    general_format = logging.Formatter('%(asctime)s %(levelname)-8s %(message)s','%Y-%m-%d %H:%M')
    logging.basicConfig(format=general_format, level=logging.WARNING)
    # Set up argument parser and parse arguments
    args = parse_args()
    # Configure logging per user arguments
    logging.getLogger().handlers = []
    logger = logging.getLogger()
    logger.setLevel(args.verbose)
    stream = logging.StreamHandler()
    if not args.quiet:
        logger.addHandler(stream)
    if args.log_file:
        log_file = os.path.abspath(args.log_file)
        log_handler = logging.FileHandler(log_file)
        logger.addHandler(log_handler)
    main(args)
