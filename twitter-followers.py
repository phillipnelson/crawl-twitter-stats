'''
Build follow graph for members of audience.

Usage:  python twitter-followers.py <username> [<audience_file>.txt]

Input:
    Twitter user's <username>
    or
    File of audience members

Output: 
    File:       <username>_followers.csv
    Format:     <user_id>,<friend_id>

'''

import sys
import twitter2
from api import twitter_api

def get_friends(user_id):
    cursor = -1
    friends = []
    try:
        while not cursor == False:
            response = twitter_api.GetFriendIDs(user=user_id,cursor=cursor)
            friends += response['ids']
            cursor =  response['next_cursor'] if len(response['ids']) else False
    except twitter2.TwitterError as exc:
        print "Error: not authorized to fetch friends for %s: %s" % (user_id,exc)
    return friends

def get_followers(user_id):
    cursor = -1
    followers = []
    try:
        while not cursor == False:
            response = twitter_api.GetFollowerIDs(userid=user_id,cursor=cursor)
            followers += response['ids']
            cursor =  response['next_cursor'] if len(response['ids']) else False
    except twitter2.TwitterError as exc:
        print "Error: not authorized to fetch friends for %s: %s" % (user_id,exc)
    return followers

def get_audience_from_file(filename):
    audience_list = []
    with open(filename) as f:
        for line in f:
            audience_list.append(get_id(line.strip()))
    return audience_list

def get_id(username):
    return twitter_api.GetUser(username).id
    
def write_friends_list(user_id,friends):
    for friend_id in friends:
        output_friends_file.write("%s,%s\r\n" % (user_id,friend_id))

def write_friends(audience_list):
    written_friends = get_friends_from_output_friends_file()
    for friend_id in audience_list:
        if friend_id not in written_friends:
            write_friends_list(friend_id,get_friends(friend_id))

def get_friends_from_output_friends_file():
    friends = [line.strip().split(',').pop(0) for line in output_friends_file]
    return list(set(friends))

if __name__ == '__main__':
    username = sys.argv[1]
    output_friends_file  = open("data/%s_audience.csv" % username, 'a+')
    if len(sys.argv) == 3:
        write_friends(get_audience_from_file(sys.argv[2]))
    else:
        write_friends(get_followers(get_id(username)))
    output_friends_file.close()
