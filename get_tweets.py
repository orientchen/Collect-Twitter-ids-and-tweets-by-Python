import tweepy  # https://github.com/tweepy/tweepy
import os
import csv
import glob
import json
import time




# if not os.path.exists(TWEETS_DIR):
#    os.makedirs(TWEETS_DIR)

# Twitter API credentials
consumer_key = "XXXXXXXXXXXXXXXXXXXXX"
consumer_secret = "XXXXXXXXXXXXXXXXXXXXX"
access_key = "XXXXXXXXXXXXXXXXXXXXX"
access_secret = "XXXXXXXXXXXXXXXXXXXXX"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)
api = tweepy.API(auth)


def get_all_tweets(id, alltweets):
    # Twitter only allows access to a users most recent 3240 tweets with this method

    # authorize twitter, initialize tweepy

    # initialize a list to hold all the tweepy Tweets

    while True:
        try:
            # make initial request for most recent tweets (200 is the maximum allowed count)
            new_tweets = api.user_timeline(id=id, count=200)
        except tweepy.TweepError as error:
            #print(type(error))
            print(error)
            if str(error) == 'Not authorized.':
                print('Can"t access user data - not authorized.')
                return alltweets

            if str(error) == 'User has been suspended.':
                print('User suspended.')
                return alltweets

            errorObj = error.args[0][0]

            print(errorObj)

            # if errorObj == 'F' or 'N':
            #    continue

            if errorObj['message'] == 'Rate limit exceeded':
                print('Rate limited. Sleeping for 15 minutes.')
                time.sleep(15 * 60 + 15)
                continue

            return alltweets
        # save most recent tweets
        alltweets.extend(new_tweets)

        if len(alltweets) > 0:
            # save the id of the oldest tweet less one
            oldest = alltweets[-1].id - 1
        else:
            pass

        # keep grabbing tweets until there are no tweets left to grab
        while len(new_tweets) > 0:
            print("getting tweets before %s" % (oldest))

            while True:
                try:
                    # all subsiquent requests use the max_id param to prevent duplicates
                    new_tweets = api.user_timeline(id=id, count=200, max_id=oldest)
                except tweepy.TweepError as error:
                    print(type(error))

                    if str(error) == 'Not authorized.':
                        print('Can"t access user data - not authorized.')
                        return alltweets

                    if str(error) == 'User has been suspended.':
                        print('User suspended.')
                        return alltweets

                    errorObj = error.args[0][0]

                    print(errorObj)

                    if errorObj['message'] == 'Rate limit exceeded':
                        print('Rate limited. Sleeping for 15 minutes.')
                        time.sleep(15 * 60 + 15)
                        continue

                    return alltweets

                # save most recent tweets
                alltweets.extend(new_tweets)
                break
            # update the id of the oldest tweet less one
            oldest = alltweets[-1].id - 1

            print("...%s tweets downloaded so far" % (len(alltweets)))

        return alltweets

from os import listdir

def find_csv_filenames( path_to_dir, suffix=".csv" ):
    filenames = listdir(path_to_dir)
    return [ filename for filename in filenames if filename.endswith(suffix) ]

if __name__ == '__main__':

    for i in range(1, 25):
        TWEETS_DIR = '/Users/xxxxxx/PycharmProjects/TwitterBotAnalyzer/tweets'
        
        if not os.path.exists(TWEETS_DIR):
            os.makedirs(TWEETS_DIR)
      
        TWITTER_FOLLOWERS_DIR_GROUPED_1stPART = '/Users/xxxxxx/PycharmProjects/TwitterBotAnalyzer/twitter-followers-grouped/'
        
        TWITTER_FOLLOWERS_DIR_GROUPED_FOLDER = 'twitter-followers-group' + str(i)
        TWITTER_FOLLOWERS_DIR_GROUPED = TWITTER_FOLLOWERS_DIR_GROUPED_1stPART + TWITTER_FOLLOWERS_DIR_GROUPED_FOLDER

        
        filenames = find_csv_filenames(TWITTER_FOLLOWERS_DIR_GROUPED)
        for name in filenames:
            # print name
            # print os.path.splitext(name)[0]
            twitter_id = os.path.splitext(name)[0]

            alltweets = []
            # pass in the username of the account you want to download
            get_all_tweets(twitter_id, alltweets)
            # transform the tweepy tweets into a 2D array that will populate the csv
            outtweets = [[tweet.id_str, tweet.created_at, tweet.text.encode("utf-8")] for tweet in alltweets]

            # write the csv
            fname = os.path.join(TWEETS_DIR, twitter_id + '.csv')
            with open(fname, 'w') as f:
                writer = csv.writer(f)
                writer.writerow(["id", "created_at", "text"])
                writer.writerows(outtweets)
            pass


