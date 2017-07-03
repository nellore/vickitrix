# vickitrix v0.1.0

`vickitrix` makes crypto trades on GDAX based on tweets. Its development and name were inspired by [@vickicryptobot](https://twitter.com/vickicryptobot), but `vickitrix` is responsive to arbitrary rules about the content of status updates on Twitter. Here's how to get it to work.

## Preliminaries

You'll need some keys and secrets and passcodes from Twitter and GDAX. `vickitrix` will store these in a config file (`~/.vickitrix/config`) on disk, but it ensures the secrets and passcodes are AES256-encrypted so evildoers who grab your laptop while you're logged in can't easily swipe working credentials.

1. Open a new browser tab, and use it to [create a new Twitter app](https://apps.twitter.com/) after logging into Twitter. Name and describe it however you like, and specify no callback URL, but note Twitter also requires you enter some well-formed website URL to finish the process. You're allowed to write something like `https://placeholder.com/placeholder`. The thing will complain if your description isn't long enough, too. So dumb.
2. Click the `Keys and Access Tokens` tab.
3. Click `Create my access token`. The tab should now display a consumer key, a consumer secret, an access token, and an access token secret. Leave this tab be for now.
4. Open a new browser tab, and use it to [visit GDAX](https://gdax.com). Log in, click your avatar on the upper right, and click `API`.
5. Create an API key with permissions to view and trade. You should now see a key, secret, and passphrase. Don't close the tab, or you'll lose the secret forever---which isn't the end of the world; you'll just have to regenerate an API key.

## Install and configure `vickitrix`
1. Run

        pip install https://github.com/nellore/vickitrix/archive/0.1.0.zip
   ...or clone the repo, `cd` into it, `pip install` the required packages [`tweepy`](http://www.tweepy.org/), [`gdax`](https://github.com/danpaquin/GDAX-Python), and [`pycrypto`](https://pypi.python.org/pypi/pycrypto), and precede all `vickitrix` commands below with `python2`. Your choice.
2. Configure `vickitrix` by running

        vickitrix configure
    This allows you to create (or overwrite) a profile with a name of your choice. (Entering nothing makes the profile name `default`, which is nice because then you won't have to specify the profile name at the command line when you `vickitrix trade`.) You'll be asked to enter credentials from the browser tabs you left open in Preliminaries. You'll also be asked to enter a password, which you'll need every time you `vickitrix trade`.
3. Grab and edit the rules in [`vickitrix/rules/vicki.py`](vickitrix/rules/vicki.py) so they do what you want. `vickitrix/rules/vicki.py` creates a Python list of dictionaries called `rules`, where each dictionary has the following keys:
    * `handles`: a list of the Twitter handles to which the rule should apply, where commas are interpreted as logical ORs. At least one of `handles` or `keywords` must be specified in a rule. However, nothing is stopping you from passing an empty list, which `vickitrix` interprets as no filter---but do this at your own peril.
    * `keywords`: a list of keywords from tweets to which the rule should apply, where commas are interpreted as logical ORs. If both `handles` and `keyword` are specified, there's a logical OR between the two lists as well.
    * `action`: either `buy` or `sell`
    * `product`: a valid [GDAX product ID](https://docs.gdax.com/#products). It looks like `<base currency>-<quote currency>`.
    * `funds`: see [Market Order Parameters](https://docs.gdax.com/#place-a-new-order) for a definition. The value may be any Python-parseable math expression involving `{available}`, which `vickitrix` takes to be the amount of the _quote_ currency available for trading in your account. At least one of `funds` or `size` must be specified in a rule.
    * `size`: see [Market Order Parameters](https://docs.gdax.com/#place-a-new-order) for a definition. The value may be any Python-parseable math expression involving `{available}`, which `vickitrix` takes to be the amount of the _base_ currency available for trading in your account.
    * `condition`: any Python-parseable expression; use `{tweet}` to refer to the content of a tweet.
With the default rules, you buy all the ETH you can when @vickicryptobot goes long, and you sell all the ETH you can when @vickicryptobot goes short.
4. Run
        
        vickitrix trade --profile <profile name goes here> --rules <path to rules file>
        
   , and enter the profile's password. Leave out the `--profile` to use the default profile, and leave out `--rules` to use the default `vickitrix/rules/vicki.py`. `vickitrix` will listen for tweets that match the conditions from the rules in `vickirules.py` and perform the specified actions.
   If after a trade's been made, the "available to trade" line makes it look like currency vanished into thin air, don't fret; this probably means the trade hasn't completed yet. You can increase the sleep time after a trade is requested and before the "available to trade" line is displayed with `--sleep`.

## Experimental rules

Check out [`vickitrix/rules/sentiment.py`](vickitrix/rules/sentiment.py), which buys (sells) a miniscule amount of ETH when the words "good" ("bad") and "ethereum" are found in a tweet. Now imagine the possibilities---what would make inventive or more effective rules? Experiment, create issues, and make pull requests!

## Contributing

Pull requests are welcome! Fork at will! If you've written a substantial contribution, and you'd like to be added as a collaborator, reach out to me.

## Disclaimer

If you use this software, you're making and/or losing money because someone or something you probably don't know tweeted, which is totally crazy. Don't take risks with money you can't afford to lose.

This software is supplied "as is" without any warranties or support. I assume no liability or responsibility for use of the software.

