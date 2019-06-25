# Social-Network-Analysis-and-Game-Theory

This repo is to share the code I used for the projects related to social network analysis and game theory. If you find this code useful in your research, please consider citing:

@INPROCEEDINGS{chenNCA2017, 
author={J. {Chen} and H. {Li} and Z. {Wu} and M. S. {Hossain}}, 
booktitle={2017 IEEE 16th International Symposium on Network Computing and Applications (NCA)}, 
title={Sentiment analysis of the correlation between regular tweets and retweets}, 
year={2017},  
pages={1-5}, 
doi={10.1109/NCA.2017.8171354}, 
ISSN={}, 
month={Oct},}


file get_followers(2018-3-27).py is a python program which can be used to crawl twitter account and collect twitter user ids.
This code was originallly posted on http://mark-kay.net/2014/08/15/network-graph-of-twitter-followers
Later this website is not available.
The code I posted here is modified based on that code.

Step 1: Create Twitter account and generate Twitter API Key, Consumer Token, Access Key for OAuth. The instruction can be found at https://themepacific.com/how-to-generate-api-key-consumer-token-access-key-for-twitter-oauth/994/
However, Twitter company change the policy very often. You can only find the basic idea from that instruction. You'll need to work through some steps by yourself.

Step 2: Create two folders, one folder is called Twitter-users and the other one is Following. The following list is stored in Following folder. The follower list is stored in Twitter-users.

Step 3: Run the code through command line with the following commands.
first cd to the directory of the python project.
then enable the venv with venv\Scripts\activate.bat (this is the case when you use pycharm in a Windows system, for macbook, use source venv/bin/activate)
python get_followers(2018-3-27).py -s aTwitterAccount -d -3

Step 4: Extract the user ids from json file by running the code followers_ids_from_json.py.

Step 5: Run get_tweets.py to collect tweets.
