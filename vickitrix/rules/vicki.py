rules = [
    {
        'handles' : ['vickicryptobot'],
        'condition' : '"ETHUSD" in {tweet} and "long" in {tweet}',
        'order' : { 
                    'side' : 'buy',
                    'type' : 'market',
                    'product_id' : 'ETH-USD',
                    'funds' : '{available[USD]}'
                }
    },
    {
        'handles' : ['vickicryptobot'],
        'condition' : '"ETHUSD" in {tweet} and "short" in {tweet}',
        'order' : { 
                    'side' : 'sell',
                    'type' : 'market',
                    'product_id' : 'ETH-USD',
                    'size' : '{available[ETH]}'
                }
    }
]
