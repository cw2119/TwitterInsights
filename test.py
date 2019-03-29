from twitter import *
from datetime import datetime, timedelta
from textblob import TextBlob
import time
import csv
import sys
import operator
import numpy as np
from flask import Flask, render_template, request
from flask import request
import webbrowser
import cgi

#Function makes use of Twitter api to retrieve tweets based on search term passed in

    #authentication for the twitter api
t = Twitter(
        auth=OAuth('1104710748968755201-AqUjzBvEZBmKY4fchydoApwx6JueJS', 'pkTTNrKHradYCIeQayPS9c2iU7gMndWgFjVQ6azNf7JQK', '0AiTG8fZVZHX7c7grH5jJ1BCR', 'KLBcoq9vQy60w1PkCvLlavr4w9qMJrA2gO6UN32lgCnU1EqQO8'))
    #Empty list to hold all tweets
tweets_bulk = []
    #Create todays date
d = datetime.today()
    #Perform the API call 10 times, pushing tweets to the list each time
for x in range(7):
    these_tweets = t.search.tweets(q= "brexit", result_type='recent', until=d.strftime('%Y-%m-%d'), count=100)
    tweets_bulk.extend(these_tweets['statuses'])
    d = d - timedelta(days=1)
number_of_tweets_collected = len(tweets_bulk)
#returns a list of tweets that have been retrieved by search



polarity_list = []
edited_polarity_list =[]
subjectivity_list =[]
positive_tweets = 0
negative_tweets = 0
for tweet in tweets_bulk:
    #Get the user object from the current tweet
    user = tweet['user']

    print "user", user, "\n\n\n\n\n"
        #getting the text of the tweet
    tweet_texts = tweet['text']
    tweet_text = TextBlob(tweet_texts)

    for word in tweet_text.sentences:
            #polarity_list.append(word.sentiment.polarity)
            #subjectivity_list.append(word.sentiment.subjectivity)
            if word.sentiment.subjectivity>0.5 and word.sentiment.polarity<-0.2:
                negative_tweets = negative_tweets +1
            elif word.sentiment.subjectivity>0.5 and word.sentiment.polarity >0.3:
                positive_tweets = positive_tweets +1
            subjectivity_list.append(word.sentiment.subjectivity)


#for sentiments in polarity_list:
#
#    if sentiments< -0.2:
#        negative_tweets = negative_tweets +1
#    elif sentiments> 0.2:
#        positive_tweets = positive_tweets +1
subjectivity_average = np.mean(subjectivity_list)
print subjectivity_average
    #getting the average polarity
    #polarity_average = np.mean(edited_polarity_list)

occupationOccurences ={}
occupations = open("occupation_list.csv", "r")
bigString_occupations = occupations.read()
occupationList = bigString_occupations.split(',')
for tweet in tweets_bulk:
    user = tweet['user']
    bio = user['description']
    for occupation in occupationList:
        if occupation.lower() in bio.lower():
            if occupation in occupationOccurences:
                occupationOccurences[occupation] = occupationOccurences[occupation] +1
            else:
                occupationOccurences[occupation]=1
            
print occupationOccurences

print "positive:", positive_tweets
print "negative;", negative_tweets
