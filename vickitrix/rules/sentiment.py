rules = [
    {
        'keywords' : ['ethereum', 'good'],
        'condition' : '"good" in {tweet} and "ethereum" in {tweet}',
        'orders' : [
            { 
                'side' : 'buy',
                'type' : 'market',
                'product_id' : 'ETH-USD',
                'funds' : '{available[USD]}*0.001'
            }
        ]
    },
    {
        'keywords' : ['ethereum', 'bad'],
        'condition' : '"bad" in {tweet} and "ethereum" in {tweet}',
        'orders' : [
            { 
                'side' : 'sell',
                'type' : 'market',
                'product_id' : 'ETH-USD',
                'size' : '{available[ETH]}*0.0001'
            }
        ]
    }
]
