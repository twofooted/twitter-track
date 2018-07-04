# Twitter Tracker
This is a simple program to pull down tweets based on the seach query and determine the rate at which that subject is being tweeted about. The idea is to log the rate with a timestamp and, if you choose, to save the tweets which have been pulled down into a json file.

This uses vanilla Python with [python-twitter](https://python-twitter.readthedocs.io/en/latest/)

The only setup that is needed is to register on [Twitter](https://developer.twitter.com/en.html) as a developer and get your access keys and tokens. Then replace the following placeholders with your information.
```python
api = twitter.Api(consumer_key='YOUR_CONSUMER_KEY',
                  consumer_secret='YOUR_CONSUMER_SECRET_KEY',
                  access_token_key='YOUR_ACCESS_TOKEN_KEY',
                  access_token_secret='YOUR_ACCESS_TOKEN_SECRET_KEY')
```