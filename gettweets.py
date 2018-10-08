import os
import sys
import tweepy
from tweepy import OAuthHandler
from tweepy import API
from tweepy import cursor
import json

path = 'D:/MyFolder/TwitterFiles'
os.chdir(path)

# Here you need to put the 4 API keys you got from tweeter
consumer_key = ''
consumer_secret = ''
access_token = ''
access_secret = ''
 
auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
 
'''
We added wait_on_rate_limit due to the error 429 code is returned when a request cannot be served due to the application’s rate limit having been 
exhausted for the resource.(from documentation) 
we suppose this  problem regards not the quantity of data but the frequency.
the 429 code is returned when a request cannot be served due to the application’s rate limit having been exhausted for the resource.(from documentation) 
Rate limits are divided into 15 minute intervals. All endpoints require authentication, so there is no concept of unauthenticated calls and rate limits.
There are two initial buckets available for GET requests: 15 calls every 15 minutes, and 180 calls every 15 minutes.
So adding wait_on_rate_limit=True this will make the rest of the code obey the rate limit
Reference https://stackoverflow.com/questions/41786569/twitter-error-code-429-with-tweepy
'''
api = tweepy.API(auth, wait_on_rate_limit=True)


'''
Without this we will get error indicates that the tweet from the timeline contains non BMP unicode characters like for example emoji.
(\U0001F600 represents the unicode character U+1F600 grinning face).
The error is indeed caused by Tk not supporting unicode characters with code greater than FFFF. A simple workaround is the filter them out of your string.
'\ufffd' is the Python representation for the unicode U+FFFD REPLACEMENT CHARACTER.
Reference https://stackoverflow.com/questions/45715280/ucs-2-codec-cant-encode-characters-in-position-61-61?rq=1
'''
def BMP(s):
    return "".join((i if ord(i) < 10000 else '\ufffd' for i in s))

'''
i = 1
# read our timeline (Twitter homepage) we can get up to 800 recent tweets from the home timeline and if we use the user timeline method we can get up
# to 3200 tweets
for status in tweepy.Cursor(api.home_timeline).items(50):
    #Process a single status
    print('Tweet # ', i)
    i+=1
    print(BMP(status.text),'\n')
'''

#open file to write tweets in it.
#if the file not exist it will create it, and if it is exist it will add to the same file.
savefile=open('tweets3.txt','a+')


i = 1 #counter only to track the progress.

# read our timeline (Twitter homepage) we can get up to 800 recent tweets from the home timeline and if we use the user timeline method we can get up
# to 3200 tweets
# read from account
for status in tweepy.Cursor(api.user_timeline, screen_name='@realDonaldTrump').items():
    #Process a single status
    print('Tweet # ', i)
    i+=1
    print(BMP(status.text),'\n')
    savefile.write(json.dumps(status._json)+'\n')

savefile.close()
