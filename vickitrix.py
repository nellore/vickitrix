#!/usr/bin/env python
"""
vickitrix

Periodically checks tweets of @vickicryptobot. If she's going short, uses 
GDAX API (via https://github.com/danpaquin/GDAX-Python) to sell specified
percentage of stack, and if she's going long, buys specified 
percentage of stack.
"""
try:
    import gdax
except ImportError:
    raise ImportError(
        'vickitrix requires GDAX-Python. Install it with "pip install gdax".'
    )

if __name__ == '__main__':
    