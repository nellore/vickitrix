rules = [
    {
        'handles' : ['vickicryptobot'],
        'action' : 'buy',
        'product' : 'ETH-USD',
        'funds' : '{available}',
        'condition' : '"ETHUSD" in {tweet} and "long" in {tweet}'
    },
    {
        'handles' : ['vickicryptobot'],
        'action' : 'sell',
        'product' : 'ETH-USD',
        'size' : '{available}',
        'condition' : '"ETHUSD" in {tweet} and "short" in {tweet}'
    }
]
