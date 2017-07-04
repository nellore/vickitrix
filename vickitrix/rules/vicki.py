rules = [
    {
        'handles' : ['Vickicryptobot'],
        'condition' : '"ETHUSD" in {tweet} and "long" in {tweet}',
        'orders' : [
            { 
                'side' : 'buy',
                'type' : 'market',
                'product_id' : 'ETH-USD',
                'funds' : '{available[USD]}'
            }
        ]
    },
    {
        'handles' : ['Vickicryptobot'],
        'condition' : '"ETHUSD" in {tweet} and "short" in {tweet}',
        'orders' : [
            { 
                'side' : 'sell',
                'type' : 'market',
                'product_id' : 'ETH-USD',
                'size' : '{available[ETH]}'
            }
        ]
    }
]
