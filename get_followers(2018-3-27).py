# -*- coding: utf-8 -*-
import tweepy
import time
import os
import sys
import json
import argparse

import urllib3
urllib3.disable_warnings()


###The directory ‘following’ contains a CSV file for each twitter account queried.
###The name of each file is the screen name of the twitter account and
###the content is a tab delimited list, each row contains the twitter id,
###screen name and account name of a follower, up to a maximum of 200 followers.


###The second directory is called ‘twitter-users’, it is a cache of twitter user details,
###each file contains cached data for a twitter user including friend and follower counts and
###a list of follower IDs (up to a maximum of 5000 follower IDs can be queried from the API).

FOLLOWING_DIR = 'C:/Users/jundong.chen/Documents/Following'
MAX_FRIENDS = 200
FRIENDS_OF_FRIENDS_LIMIT = 200

if not os.path.exists(FOLLOWING_DIR):
    #os.makedir(FOLLOWING_DIR)
    os.makedirs(FOLLOWING_DIR)

enc = lambda x: x.encode('ascii', errors='ignore')



CONSUMER_KEY = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
CONSUMER_SECRET = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'

# The access tokens can be found on your applications's Details
# page located at https://dev.twitter.com/apps (located
# under "Your access token")
ACCESS_TOKEN = 'XXXXXXXXXXXXXXX-XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
ACCESS_TOKEN_SECRET = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'

# == OAuth Authentication ==
#
# This mode of authentication is the new preferred way
# of authenticating with Twitter.
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

api = tweepy.API(auth)

def get_follower_ids(centre, max_depth=1, current_depth=0, taboo_list=[]):

    # print 'current depth: %d, max depth: %d' % (current_depth, max_depth)
    # print 'taboo list: ', ','.join([ str(i) for i in taboo_list ])

    if current_depth == max_depth:
        print('out of depth')
        return taboo_list

    if centre in taboo_list:
        # we've been here before
        print('Already been here.')
        return taboo_list
    else:
        taboo_list.append(centre)

    try:
        userfname = os.path.join('C:/Users/jundong.chen/Documents/Twitter-users/', str(centre) + '.json')
        if not os.path.exists(userfname):
            print('Retrieving user details for twitter id %s' % str(centre))
            while True:
                try:
                    user = api.get_user(centre)

                    d = {'name': user.name,
                         'screen_name': user.screen_name,
                         'id': user.id,
                         'friends_count': user.friends_count,
                         'followers_count': user.followers_count,
                         'followers_ids': user.followers_ids()}

                    with open(userfname, 'w') as outf:
                        outf.write(json.dumps(d, indent=1))

                    user = d
                    break
                except tweepy.TweepError as error:
                    print(type(error))

                    if str(error) == 'Not authorized.':
                        print('Can''t access user data - not authorized.')
                        return taboo_list

                    if str(error) == 'User has been suspended.':
                        print('User suspended.')
                        return taboo_list

                    errorObj = error.args[0][0]

                    print(errorObj)

                    if errorObj['message'] == 'Rate limit exceeded':
                        print('Rate limited. Sleeping for 15 minutes.')
                        time.sleep(15 * 60 + 15)
                        continue

                    return taboo_list
        else:
            #user = json.loads(file(userfname).read())
            with open(userfname, encoding='utf-8') as data_file:
                user = json.loads(data_file.read())
        screen_name = enc(user['screen_name'])

        print(type(FOLLOWING_DIR))
        print(type(screen_name))
        print('.csv')
        fname = os.path.join(FOLLOWING_DIR.encode("utf-8"), screen_name + '.csv'.encode("utf-8"))
        friendids = []

        # only retrieve friends of TED... screen names
        #if screen_name.startswith('TED'):
        if not os.path.exists(fname):
            print('No cached data for screen name "%s"' % screen_name)
            with open(fname, 'w') as outf:
                params = (enc(user['name']), screen_name)
                print('Retrieving friends for user "%s" (%s)' % params)

                    # page over friends
                c = tweepy.Cursor(api.friends, id=user['id']).items()

                friend_count = 0
                while True:
                    try:
                        friend = c.next()
                        friendids.append(friend.id)
                        params = (friend.id, enc(friend.screen_name), enc(friend.name))
                        outf.write('%s\t%s\t%s\n' % params)
                        friend_count += 1
                        if friend_count >= MAX_FRIENDS:
                            print('Reached max no. of friends for "%s".' % friend.screen_name)
                            break
                    except tweepy.TweepError:
                            # hit rate limit, sleep for 15 minutes
                        print('Rate limited. Sleeping for 15 minutes.')
                        time.sleep(15 * 60 + 15)
                        continue
                    except StopIteration:
                        break
        else:
            with open(fname, 'r') as readf:
                friendids = [int(line.strip().split('\t')[0]) for line in readf]

        print('Found %d friends for %s' % (len(friendids), screen_name))

            # get friends of friends
        cd = current_depth
        if cd+1 < max_depth:
            for fid in friendids[:FRIENDS_OF_FRIENDS_LIMIT]:
                taboo_list = get_follower_ids(fid, max_depth=max_depth,
                    current_depth=cd+1, taboo_list=taboo_list)

        if cd+1 < max_depth and len(friendids) > FRIENDS_OF_FRIENDS_LIMIT:
            print('Not all friends retrieved for %s.' % screen_name)

    except Exception as error:
        print('Error retrieving followers for user id: ', centre)
        print(error)

        if os.path.exists(fname):
            os.remove(fname)
            print('Removed file "%s".' % fname)

        sys.exit(1)

    return taboo_list

#get_follower_ids('TEDxSingapore',1, 3 )
#get_follower_ids('orientchen1978',1, 3 )
if __name__ == '__main__':
     ap = argparse.ArgumentParser()
     ap.add_argument("-s", "--screen-name", required=True, help="Screen name of twitter user")
     ap.add_argument("-d", "--depth", required=True, type=int, help="How far to follow user network")
     args = vars(ap.parse_args())

     twitter_screenname = args['screen_name']
     depth = int(args['depth'])

     if depth < 1 or depth > 3:
         print('Depth value %d is not valid. Valid range is 1-3.' % depth)
         sys.exit('Invalid depth argument.')

     print('Max Depth: %d' % depth)
     matches = api.lookup_users(screen_names=[twitter_screenname])

     if len(matches) == 1:
         print(get_follower_ids(matches[0].id, max_depth=depth))
     else:
         print('Sorry, could not find twitter user with screen name: %s' % twitter_screenname)
