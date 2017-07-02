#!/usr/bin/env python
"""
vickitrix

Periodically checks tweets of @vickicryptobot using 
https://github.com/bear/python-twitter. If she's going short, uses 
GDAX API (via https://github.com/danpaquin/GDAX-Python) to sell specified
percentage of ETH stack, and if she's going long, buys specified 
percentage of USD stack.
"""

_help_intro = (
"""vickitrix bases GDAX ETHUSD trades on @vickicryptobot's tweets.
"""
    )

try:
    import gdax
except ImportError:
    raise ImportError(
        'vickitrix requires GDAX-Python. Install it with "pip install gdax".'
    )

try:
    import twitter
except ImportError:
    raise ImportError(
        'vickitrix requires python-twitter. Install it with '
        '"pip install python-twitter".'
    )

import os
import errno
import time
import argparse
from argparse import HelpFormatter
import getpass
import datetime
import sys

def help_formatter(prog):
    """ So formatter_class's max_help_position can be changed. """
    return HelpFormatter(prog, max_help_position=40)

def get_dough(gdax_client):
    """ Retrieve dough in user accounts

        gdax_client: instance of gdax.AuthenticatedClient

        Return value: dictionary mapping currency to account information
    """
    dough = {}
    for account in gdax_client.get_accounts():
        dough[account['currency']] = account['available']
    return dough

def print_to_screen(message, newline=True, carriage_return=False):
    """ Prints message to stdout as well as stderr if stderr is redirected.

        message: message to print
        newline: True iff newline should be printed
        carriage_return: True iff carriage return should be printed; also
            clears line with ANSI escape code

        No return value.
    """
    full_message = ('\x1b[K' + message + ('\r' if carriage_return else '')
                        + ('\n' if newline else ''))
    try:
        sys.stderr.write(full_message)
        if sys.stderr.isatty():
            sys.stderr.flush()
        else:
            try:
                # So the user sees it too
                sys.stdout.write(full_message)
                sys.stdout.flush()
            except UnicodeEncodeError:
                sys.stdout.write(
                                unicodedata.normalize(
                                        'NFKD', full_message
                                    ).encode('ascii', 'ignore')
                            )
                sys.stdout.flush()
    except UnicodeEncodeError:
        sys.stderr.write(
                        unicodedata.normalize(
                                'NFKD', full_message
                            ).encode('ascii', 'ignore')
                    )
        sys.stderr.flush()


if __name__ == '__main__':
    if not (sys.version_info >= (2,7) and sys.version_info[0] == 2):
        raise RuntimeError('Vickitrix should be run using Python 2.7.x.')
    # Print file's docstring if -h is invoked
    parser = argparse.ArgumentParser(description=_help_intro, 
                formatter_class=help_formatter)
    subparsers = parser.add_subparsers(help=(
                'subcommands; add "-h" or "--help" '
                'after a subcommand for its parameters'),
                dest='subparser_name'
            )
    config_parser = subparsers.add_parser(
                            'config',
                            help=(
                                'creates profile for storing API keys; '
                                'all keys are stored in ~/.vickitrix/config'
                            )
                        )
    trade_parser = subparsers.add_parser(
                            'trade',
                            help='trades ETHUSD inspired by @vickicryptobot'
                        )
    # Add command-line arguments
    config_parser.add_argument('--sell-stack-pct', '-s', type=float,
            required=False,
            default=100,
            help=('approximate percentage of ETH stack to sell for USD when '
                  'Vicki goes short')
        )
    config_parser.add_argument('--buy-stack-pct', '-b', type=float,
            required=False,
            default=100,
            help=('approximate percentage of USD stack to use to buy ETH when '
                  'Vicki goes long')
        )
    trade_parser.add_argument('--profile', '-p', type=str, required=False,
            default='default',
            help='which profile to use for trading'
        )
    trade_parser.add_argument('--period', type=int, required=False,
            default=90,
            help=('how often (in s) to check Twitter for an update '
                  'from @vickicryptobot')
        )
    trade_parser.add_argument('--retries', type=int, required=False,
            default=3,
            help=('how many times to reattempt communicating with Twitter or '
                  'GDAX before bailing')
        )
    args = parser.parse_args()
    key_dir = os.path.expanduser('~/.vickitrix')
    if args.subparser_name == 'config':
        try:
            os.makedirs(key_dir)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise
        # Grab and write all necessary credentials
        config_file = os.path.join(key_dir, 'config')
        print 'Enter a name for this profile (default): ',
        profile_name = raw_input()
        if not profile_name: profile_name = 'default'
        with open(config_file, 'a') as config_stream:
            print >>config_stream, ''.join(['[', profile_name, ']'])
            for token in ['GDAX key', 'GDAX secret', 'GDAX passphrase',
                            'Twitter consumer key', 'Twitter consumer secret',
                            'Twitter access token key',
                            'Twitter access token secret']:
                print >>config_stream, getpass.getpass(
                                    ''.join(['Enter ', token, ': '])
                                )
    elif args.subparser_name == 'trade':
        # Use _last_ entry in config file with profile name
        with open(os.path.join(key_dir, 'config')) as config_stream:
            line = config_stream.readline()
            while line:
                stripped = line.strip()
                if stripped.startswith('[') and stripped.endswith(']'):
                    profile_name = stripped[1:-1]
                if profile_name == args.profile:
                    [gdax_key, gdax_secret, gdax_passphrase,
                        consumer_key, consumer_secret,
                        access_token_key, access_token_secret] = [
                                config_stream.readline().strip()
                                for _ in xrange(7)
                            ]
                else:
                    for _ in xrange(6):
                        config_stream.readline()
                line = config_stream.readline()
        # Instantiate GDAX and Twitter clients
        gdax_client = gdax.AuthenticatedClient(
                                gdax_key, gdax_secret,
                                gdax_passphrase
                            )
        twitter_client = twitter.Api(
                    consumer_key=consumer_key,
                    consumer_secret=consumer_secret,
                    access_token_key=access_token_key,
                    access_token_secret=access_token_secret
                )
        try:
            last_status = twitter_client.GetUserTimeline(
                                            screen_name='vickicryptobot'
                                        )[0]
        except IndexError:
            raise RuntimeError('@vickicryptobot doesn\'t appear to have any '
                               'tweets on her timeline, which is strange....')
        while True:
            time.sleep(args.period)
            next_status = twitter_client.GetUserTimeline(
                                            screen_name='vickicryptobot'
                                        )[0]
            if next_status['id'] != last_status['id']:
                print_to_screen(
                        'Retrieved {:%Y-%m-%d %H:%M:%S}; @vickibot: '
                    ).format(datetime.datetime.now()) + last_status['text']
                last_status = next_status
                if 'ETHUSD' in last_status['text']:
                    # Hurrah! We should trade. Grab how much dough's available.
                    dough = get_dough(gdax_client)
                    if 'short' in last_status:
                        # Sell ETH
                        amount = float(int(float(
                                dough['ETH']
                            ) * args.sell_stack_pct)) / 100
                        if amount == 0: continue
                        print_to_screen('Selling {} ETH...'.format(amount))
                        gdax_client.sell(
                                type='market',
                                product_id='ETH-USD',
                                size=str(amount) # ETH
                            )
                        time.sleep(10)
                        print_to_screen('Sold {} ETH.'.format(amount))
                        dough = get_dough(gdax_client)
                        print_to_screen(
                                ('You have ${} and {} '
                                 'ETH available to trade.').format(
                                        dough['USD'], dough['ETH']
                                    )
                            )
                    elif 'long' in last_status:
                        # Buy ETH
                        amount = float(int(float(
                                dough['USD']
                            ) * args.buy_stack_pct)) / 100
                        if amount == 0: continue
                        print_to_screen('Buying ${} worth of ETH...'.format(
                                                                        amount
                                                                    ))
                        gdax_client.buy(
                                type='market',
                                product_id='ETH-USD',
                                funds=str(amount)
                            )
                        time.sleep(10)
                        print_to_screen('Bought ${} worth of ETH.'.format(
                                                                        amount
                                                                    ))
                        dough = get_dough(gdax_client)
                        print_to_screen(
                                ('You have ${} and {} '
                                 'ETH available to trade.').format(
                                        dough['USD'], dough['ETH']
                                    )
                            )
