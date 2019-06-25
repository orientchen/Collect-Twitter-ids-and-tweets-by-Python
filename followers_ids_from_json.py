import json
import os
import csv
import glob



for i in range(0, 116):
    #TWITTER_USERS_DIR_GROUPED_1stPART = '/Users/orientchen/Research/TwitterHarvester/TwitterDataFromDSULaptop/twitter-users-grouped/'
    TWITTER_USERS_DIR_GROUPED_1stPART = '/Users/orientchen/Research/TwitterBotAnalyzer/FullExperiment/Twitter-users-grouped/'

    TWITTER_USERS_DIR_GROUPED_FOLDER = 'twitter-users-group' + str(i)
    TWITTER_USERS_DIR_GROUPED = TWITTER_USERS_DIR_GROUPED_1stPART + TWITTER_USERS_DIR_GROUPED_FOLDER

    TWITTER_FOLLOWERS_DIR_GROUPED_1stPART = '/Users/orientchen/Research/TwitterBotAnalyzer/FullExperiment/Twitter-followers-grouped/'
    slash = '/'
    TWITTER_FOLLOWERS_DIR_GROUPED_FOLDER = 'twitter-followers-group' + str(i)
    TWITTER_FOLLOWERS_DIR_GROUPED = TWITTER_FOLLOWERS_DIR_GROUPED_1stPART + slash + TWITTER_FOLLOWERS_DIR_GROUPED_FOLDER
    if not os.path.exists(TWITTER_FOLLOWERS_DIR_GROUPED):
        os.makedirs(TWITTER_FOLLOWERS_DIR_GROUPED)

    print(TWITTER_USERS_DIR_GROUPED)
    for f in glob.glob(os.path.join(TWITTER_USERS_DIR_GROUPED, '*.json')):
        with open(f) as twitter_file:
            #print("here")
            json_data = json.load(twitter_file)
            #print(json_data['followers_ids'])
            follower_id_list = json_data['followers_ids']
            #print(follower_id_list)

            base=os.path.basename(f)
            twitter_id = os.path.splitext(base)[0]
            print(twitter_id)
            fname = TWITTER_FOLLOWERS_DIR_GROUPED + slash + str(twitter_id) + '.csv'
            with open(fname, "w") as outfile:
                for follower_id in follower_id_list:
                    outfile.write(str(follower_id))
                    outfile.write("\n")

