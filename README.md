# vickitrix v0.1.0

`vickitrix` makes crypto trades on GDAX based on tweets. Its development and name were inspired by the Twitter bot [@vickicryptobot](https://twitter.com/vickicryptobot), but `vickitrix` is responsive to arbitrary rules about the content of selected users' status updates on Twitter. Here's how to get it to work.

## Preliminaries

You'll need some keys and secrets and passcodes from Twitter and GDAX. `vickitrix` will store these in a config file (`~/.vickitrix/config`) on disk, but it ensures the secrets and passcodes are AES256-encrypted so evildoers who grab your laptop while you're logged in can't easily swipe working credentials.

1. Open a new browser tab, and use it to [create a new Twitter app](https://apps.twitter.com/) after logging into Twitter. Name and describe it however you like, but note Twitter also requires you enter some well-formed website URL to finish the process. You're allowed to write something like `https://placeholder.com/placeholder`. The thing will complain if your description isn't long enough, too. So dumb.
2. Click the `Keys and Access Tokens` tab.
3. Click `Create my access token`. The tab should now display a consumer key, a consumer secret, an access token, and an access token secret. Leave this tab be for now.
4. Open a new browser tab, and use it to [visit GDAX](https://gdax.com). Log in, click your avatar on the upper right, and click `API`.
5. Create an API key with permissions to view and trade. You should now see a key, secret, and passphrase. Don't close the tab, or you'll lose the secret forever---which isn't the end of the world; you'll just have to regenerate an API key.

## Install and configure `vickitrix`
1. Clone this repo and `cd` there:
        
        git clone https://github.com/nellore/vickitrix
        cd vickitrix
2. Install some required packages:

        pip install tweepy
        pip install gdax
        pip install pycrypto
3. Configure `vickitrix` by running

        python vickitrix configure
        
    This allows you to create (or overwrite) a profile with a name of your choice. (Entering nothing makes the profile name `default`, which is nice because then you won't have to specify the profile name at the command line when you turn on the `vickitrix` tweet monitor/trader.) You'll be asked to enter credentials from the browser tabs you left open in Preliminaries, so do that.
4. Edit the rules in `vickirules.py` so they do what you want. `vickirules.py` creates a Python list of dictionaries called `rules`, where each dictionary has the following keys:
    * `handle`: the Twitter handle the rule refers to
    * `action`: either `buy` or `sell`
    * `product`: a valid [GDAX product ID](https://docs.gdax.com/#products)
    * `funds`: see [Market Order Parameters](https://docs.gdax.com/#place-a-new-order) for a definition. The value may be any Python-parseable math expression involving `{available}`, which `vickitrix` takes to be the amount of the _quote_ currency available for trading in your account. At least one of `funds` or `size` must be specified in a rule.
    * `size`: see [Market Order Parameters](https://docs.gdax.com/#place-a-new-order) for a definition. The value may be any Python-parseable math expression involving `{available}`, which `vickitrix` takes to be the amount of the _base_ currency available for trading in your account. At least one of `funds` or `size` must be specified in a rule.
    * `condition`: any Python-parseable expression; use `{tweet}` to refer to the content of a tweet.
With the default rules, you buy all the ETH you can when @vickicryptobot goes long, and you sell all the ETH you can when @vickicryptobot goes short.
5. Run
        python vickitrix trade --profile <profile name goes here> --rules <path to rules file>
        
   Leave out the `--profile` to use the default profile, and `--rules` to use the `rules.py` file in the same directory as the `vickitrix` script.
