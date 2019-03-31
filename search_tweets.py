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
import json
import os
import urllib2

#Function makes use of Twitter api to retrieve tweets based on search term passed in
def get_tweets(search_term):
    #authentication for the twitter api
    t = Twitter(
        auth=OAuth('1104710748968755201-AqUjzBvEZBmKY4fchydoApwx6JueJS', 'pkTTNrKHradYCIeQayPS9c2iU7gMndWgFjVQ6azNf7JQK', '0AiTG8fZVZHX7c7grH5jJ1BCR', 'KLBcoq9vQy60w1PkCvLlavr4w9qMJrA2gO6UN32lgCnU1EqQO8'))
    #Empty list to hold all tweets
    tweets_bulk = []
    #Create todays date
    d = datetime.today()
    #Perform the API call 10 times, pushing tweets to the list each time
    for x in range(7):
        these_tweets = t.search.tweets(q= search_term, result_type='recent', until=d.strftime('%Y-%m-%d'), count=100)
        tweets_bulk.extend(these_tweets['statuses'])
        d = d - timedelta(days=1)
    number_of_tweets_collected = len(tweets_bulk)
#returns a list of tweets that have been retrieved by search
    return tweets_bulk

def get_gender_ratio(tweets):
    female_count = 0
    male_count = 0
    for tweet in tweets:
        #Get the user object from the current tweet
        user = tweet['user']
        #get their name from user
        name = user['name']
        #send the name to the getGender method to find out if it is male or female
        gender = getGender(name)
        #depending on whether name is male or female, add to count
        if gender == 'male':
            male_count = male_count + 1
        if gender == 'female':
            female_count = female_count + 1
#returning ratio of male:female
    return str(male_count) + ":" + str(female_count)




def getGender(name):
    #make names all lower case and take away surnames
    trimmedName = (name.partition(' ')[0]).lower()
    #importing list of female names from csv file
    file_female = open("female_names.csv", "r")
    bigString_female = file_female.read()
    femaleNames = bigString_female.split(',')
    #importing list of male names from csv file
    file_male = open("male_names.csv", "r")
    bigString_male = file_male.read()
    maleNames = bigString_male.split(',')

    #looping each name through the list of female names and looking for a match
    for femaleName in femaleNames:
        if trimmedName == femaleName.lower():
            return "female"
    #looping each name through the list of male names and looking for a match
    for maleName in maleNames:
        if trimmedName == maleName.lower():
            return "male"
    return "none"

def getCountry(tweets):
    country_list = []
    top_ten_countries_list = []
    #a dict for the locations and number of hits per location
    country_occurences = {}
    for tweet in tweets:
        #Get the user object from the current tweet
        user = tweet['user']
        #removing tweets with location services switched off
        if user['location'] != '':
            user_country = user['location']
            if user_country in country_occurences:
                country_occurences[user_country] = country_occurences[user_country] +1
            else:
                country_occurences[user_country]=1
        #sorting the dict of countries
        sorted_country_occurences = sorted(country_occurences.items(), key=operator.itemgetter(1))
        #adding the 10 most common countries tweeted from to a list
        top_ten_countries_list = sorted_country_occurences[-5:]
    return top_ten_countries_list

def getSentiment(tweets):
    polarity_list = []
    subjectivity_list =[]
    positive_tweets = 0
    negative_tweets = 0
    for tweet in tweets:
        #Get the user object from the current tweet
        user = tweet['user']
        #getting the text of the tweet
        tweet_texts = tweet['text']
        tweet_text = TextBlob(tweet_texts)
        #getting the polarity for each sentiment and adding this to a list
        for word in tweet_text.sentences:
                #polarity_list.append(word.sentiment.polarity)
                #subjectivity_list.append(word.sentiment.subjectivity)
                if word.sentiment.subjectivity>0.6 and word.sentiment.polarity<-0.2:
                    negative_tweets = negative_tweets +1
                elif word.sentiment.subjectivity>0.6 and word.sentiment.polarity >0.3:
                    positive_tweets = positive_tweets +1
                subjectivity_list.append(word.sentiment.subjectivity)
        subjectivity_average = np.mean(subjectivity_list)
        return subjectivity_average

def getOccupation(tweets):
    occupationOccurences ={}
    occupations = open("occupation_list.csv", "r")
    bigString_occupations = occupations.read()
    occupationList = bigString_occupations.split(',')
    for tweet in tweets:
        user = tweet['user']
        bio = user['description']
        for occupation in occupationList:
            if occupation.lower() in bio.lower():
                if occupation in occupationOccurences:
                    occupationOccurences[occupation] = occupationOccurences[occupation] +1
                else:
                    occupationOccurences[occupation]=1
    sorted_occupation_occurences = sorted(occupationOccurences.items(), key=operator.itemgetter(1))
    top_five_occupation = sorted_occupation_occurences[-5:]
    return top_five_occupation

def getTopInfluentialTweets(tweets):
    most_influential = {}

    tweets.sort(key=lambda x: x['retweet_count'], reverse=True)
    tweet_id = tweets[0]["id"]
    #Request HTML from twitterAPI
    contents = urllib2.urlopen("https://publish.twitter.com/oembed?url=https%3A%2F%2Ftwitter.com%2Ftwitter%2Fstatus%2F"+str(tweet_id)).read()

    embeddedContents = json.loads(contents)

    return embeddedContents['html']

app = Flask(__name__)
@app.route('/')
def index():
    return render_template('get_user_input.html')

@app.route('/retrieveTweetData', methods=['POST'])
def hello():
    keyword_for_search = request.form['get_keyword_for_search']
    #passing key word to get_tweets
    tweets = get_tweets(keyword_for_search)
    gender_ratio = get_gender_ratio(tweets)
    print "gender ratio = ",gender_ratio
    ten_countries = getCountry(tweets)
    print "10 countries = ", ten_countries
    #polarity = getSentiment(tweets)
    #print "polarity = ",polarity
    occupation = getOccupation(tweets)
    print "occupation:", occupation
    influentialTweet = getTopInfluentialTweets(tweets)
    return render_template('results.html', influentialTweet = influentialTweet, ratio=gender_ratio, tenCountries=json.dumps(ten_countries), occupation=json.dumps(occupation))
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host = '0.0.0.0', port = port)
