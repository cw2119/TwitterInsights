from twitter import *

#authentication for the twitter api
t = Twitter(
    auth=OAuth('1104710748968755201-AqUjzBvEZBmKY4fchydoApwx6JueJS', 'pkTTNrKHradYCIeQayPS9c2iU7gMndWgFjVQ6azNf7JQK', '0AiTG8fZVZHX7c7grH5jJ1BCR', 'KLBcoq9vQy60w1PkCvLlavr4w9qMJrA2gO6UN32lgCnU1EqQO8'))

tweets_bulk =  t.search.tweets(q="#trump", count=100)

#print tweets_bulk['statuses']

#making the tweets_bulk information so it contains just the statuses of them
tweets= tweets_bulk['statuses']

female_count = 0
male_count = 0

for tweet in tweets:

    #Get the user object from the current tweet
    user = tweet['user']

    #Retrieve their name
    name = user['name']

    gender = getGender(name)

#    print 'Gender:', gender, ' name: ', name

    if gender == 'male':
        male_count = male_count + 1

    if gender == 'female':
        female_count = female_count + 1



print tweets

print "number of males:", male_count
print "number of females:", female_count
