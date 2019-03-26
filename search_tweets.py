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




#f = open('get_user_input.html','w')
#message = """<html>
#<form action ="" method= "POST">
  #keyword for search:<br>
#  <input type = "text" name ="keyword_for_search"><br>
 # <input type="submit" value="Submit">
#</form>
#</html>"""

#f.write(message)
#f.close()
#get_user_input = 'file:///Macintosh HD/Users/Cici/Documents/CFG/CodeFirstGirls/Twitter_stuff/' + 'get_user_input.html'
#webbrowser.open_new_tab(get_user_input)

#form = cgi.FieldStorage()
#keyword_for_search =form.getvalue('keyword_for_search').capitilize()
#def get_keyword_for_search():
 #  if request.method == 'POST':
#        keyword_for_search = request.form['key word for search']
#        return keyword_for_search
#    else:
#        return "none"
#if user_input.html == '__main__':
#    app.run(host='0.0.0.0')

app = Flask(__name__)
@app.route('/')
def index():
    return render_template('get_user_input.html')
@app.route('/hello', methods=['POST'])
def hello():
    keyword_for_search = request.form['get_keyword_for_search']
    return keyword_for_search
if __name__ == '__main__':
    app.run(host = '0.0.0.0', port = 5000)

hello()


def getGender(name):

#
    trimmedName = (name.partition(' ')[0]).lower()

    file_female = open("female_names.csv", "r")
    bigString_female = file_female.read()
    femaleNames = bigString_female.split(',')

    file_male = open("male_names.csv", "r")
    bigString_male = file_male.read()
    maleNames = bigString_male.split(',')



    for femaleName in femaleNames:
        if trimmedName == femaleName.lower():
            return "female"

    for maleName in maleNames:
        if trimmedName == maleName.lower():
            return "male"

    return "none"

#authentication for the twitter api
t = Twitter(
    auth=OAuth('1104710748968755201-AqUjzBvEZBmKY4fchydoApwx6JueJS', 'pkTTNrKHradYCIeQayPS9c2iU7gMndWgFjVQ6azNf7JQK', '0AiTG8fZVZHX7c7grH5jJ1BCR', 'KLBcoq9vQy60w1PkCvLlavr4w9qMJrA2gO6UN32lgCnU1EqQO8'))

#search_hashtag = raw_input("what do you want to search for?")

#Empty list to hold all tweets
tweets_bulk = []

#Create todays date
d = datetime.today()

print ("Date today", d)

#Perform the API call 10 times, pushing tweets to the list each time
for x in range(7):
    these_tweets = t.search.tweets(q= keyword_for_search, result_type='recent', until=d.strftime('%Y-%m-%d'), count=100)
    tweets_bulk.extend(these_tweets['statuses'])
    d = d - timedelta(days=1)
    #time.sleep(0.3)
#print tweets_bulk['statuses']

female_count = 0
male_count = 0
country_list = []
top_ten_countries_list = []

country_occurences = {}
polarity_list = []



print "Number of tweets collected: ", len(tweets_bulk)

for tweet in tweets_bulk:

    #Get the user object from the current tweet
    user = tweet['user']


    if user['location'] != '':
        user_country = user['location']
        if user_country in country_occurences:
            country_occurences[user_country] = country_occurences[user_country] +1
        else:
            country_occurences[user_country]=1

    #Retrieve their name
    name = user['name']

    gender = getGender(name)

    if gender == 'male':
        male_count = male_count + 1

    if gender == 'female':
        female_count = female_count + 1

    tweet_texts = tweet['text']
    tweet_text = TextBlob(tweet_texts)
    for sentence in tweet_text.sentences:
        polarity_list.append(sentence.sentiment.polarity)


sorted_country_occurences = sorted(country_occurences.items(), key=operator.itemgetter(1))
top_ten_countries_list = sorted_country_occurences[-10:]
#print "Top 10 countries: ", top_ten_countries_list

#print "country occurences", country_occurences
#print tweets

print "Polarity average: ", np.mean(polarity_list)

print "number of males:", male_count
print "number of females:", female_count
