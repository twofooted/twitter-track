import twitter
import json
import time
import datetime

"""
Twitter track which uses the python-twitter package to get tweets and calculates the
tweet rate at any given time

@author Tyler Lloyd

"""

# Setup your keys
api = twitter.Api(consumer_key='YOUR_CONSUMER_KEY',
                  consumer_secret='YOUR_CONSUMER_SECRET_KEY',
                  access_token_key='YOUR_ACCESS_TOKEN_KEY',
                  access_token_secret='YOUR_ACCESS_TOKEN_SECRET_KEY')

# Baseline data
since = 0
requests = 0
stack = {}

while True:
    
    try:
        trends = api.GetSearch(raw_query='q=%40wojespn&count=100&result_type=recent', since_id=since, result_type="recent")
    except twitter.error.TwitterError:
        print("Error. Waiting for 2 min and re-trying")
        time.sleep(120)
        continue
    
    print("Most current ID: {}".format(since))
    prev_stack_size = len(stack)

    # Sets the top result as the most recent Twitter id to use on the next search
    # and loads each tweet into the stack object as a dictionary
    for trend in trends:
        id = trend.id
        obj = trend.AsDict()
        stack[id] = obj
        since = max(id, since)

    # calculate the size between the previous search and the current search
    # and uses that as the rate
    per_second_rate = (len(stack) - prev_stack_size) / 6.0
    rate = per_second_rate * 60.0

    # record the results of the rate in a file in the same directory
    rateFile = open("log.txt", 'a')
    rateFile.write("{time}, {rate}\n".format(time=datetime.datetime.now(), rate=rate))
    rateFile.close()
    
    print("Current @wojespn Tweet Rate: {} tweets/min".format(rate))
    print("Current stack is: {}".format(len(stack)))

    # After 1k new tweets have eventually been loaded this
    # stores the oldest 900 into a new file. It keeps the most recent 100
    # so that the rate stays consistent and doesn't jump up simply by loading
    # a brand new 100 instantly on the next pass
    if len(stack) >= 1000:
        temp_stack = {}
        stack_keys = list(stack.keys())
        
        for _ in range(100):
            k = stack_keys.pop()
            temp_stack[k] = stack.pop(k)
        
        now = datetime.datetime.now()
        print("{}\tBuilding new batch. {} tweets saved".format(now, len(stack)))
        fp = open("data/{0}_datadump.json".format(time.time()), 'x')

        fp.write(json.dumps(stack))
        fp.close()
        stack = temp_stack
    
    requests = requests + 1
    print("Total Calls: {}".format(requests))
    print("")
    time.sleep(6)
