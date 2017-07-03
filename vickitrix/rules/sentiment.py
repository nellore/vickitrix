rules = [
    {
        'keywords' : ['ethereum', 'good'],
        'action' : 'buy',
        'product' : 'ETH-USD',
        'funds' : '{available}*0.001',
        'condition' : '"good" in {tweet} and "ethereum" in {tweet}'
    },
    {
        'keywords' : ['ethereum', 'bad'],
        'action' : 'sell',
        'product' : 'ETH-USD',
        'size' : '{available}*0.001',
        'condition' : '"bad" in {tweet} and "ethereum" in {tweet}'
    }
]
