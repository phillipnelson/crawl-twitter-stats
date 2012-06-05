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
import math

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
    usernames = []
    with open(filename) as f:
        for line in f:
            usernames.append(line.strip())
    return get_ids(usernames)

def get_id(username):
    return twitter_api.GetUser(username).id

def get_ids(usernames):
    user_ids = []
    for n in range(int(math.ceil(len(usernames) / float(100)))):
        usernames_batch = usernames[n*100:(n+1)*100]
        response = twitter_api.UsersLookup(screen_name=usernames_batch)
        for user in response:
            user_ids.append(user.id)
    return user_ids
    
def write_friends_list(user_id,friends):
    for friend_id in friends:
        output_friends_file.write("%s,%s\r\n" % (user_id,friend_id))

def write_friends(audience_list):
    written_friends = get_friends_from_output_friends_file()
    print "Friends already processed: %s" % len(written_friends)
    # audience_info = get_audience_info(audience_list)
    for friend_id in audience_list:
        if friend_id not in written_friends:
            # if audience_info[friend_id]['friends_count'] < 10000 and audience_info[friend_id]['followers_count'] > 100:
            write_friends_list(friend_id,get_friends(friend_id))

def get_friends_from_output_friends_file():
    friends = [int(line.strip().split(',').pop(0)) for line in output_friends_file]
    return list(set(friends))

def get_audience_info(audience_list):
    audience_info = {}
    for n in range(int(math.ceil(len(audience_list) / float(100)))):
        audience_batch = audience_list[n*100:(n+1)*100]
        response = twitter_api.UsersLookup(user_id=audience_batch)
        for user in response:
            audience_info[user.id] = {'followers_count': user.followers_count, 'friends_count': user.friends_count}
    return audience_info

if __name__ == '__main__':
    username = sys.argv[1]
    output_friends_file  = open("%s/data/%s_audience.csv" % (sys.path[0], username), 'a+')
    if len(sys.argv) == 3:
        write_friends(get_audience_from_file(sys.argv[2]))
    else:
        write_friends(get_followers(get_id(username)))
    output_friends_file.close()
