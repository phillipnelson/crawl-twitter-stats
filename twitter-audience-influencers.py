'''
Rank the top N influencers of an set of users, ie the users that set of users follows the most

Usage:  python twitter-audience-influencers.py <audience_graph_file> <output_csv_file> [N=20]

Input:
    File of audience graph: (user1) follows (user2)
    Format:     <user_id>,<friend_id>


N number of top influencers    

Output: 
    File:       <audience_graph_file>.json
    Format:     [??]

'''

import json
import sys
import csv
import math
from api import twitter_api

def get_csv(f):
    file_input = open(f)
    return [line.strip().split(',') for line in file_input]
    
def reverse_list_items(data):
    return [[b,a] for [a,b] in data]

def top_n_influential(input_graph, num):
    last = None
    stack = []
    
    # Friend user tuples have been reversed and sorted
    for (friend,user) in input_graph:
        if not friend == last or [friend,user] == input_graph[-1]:
            if last:
                stack.append([count, last])						# list count first for sorting
            count = 0
        last = friend
        count += 1
    
    stack.sort()
    stack.reverse()
    return reverse_list_items(stack[0:num])

def top_n_relations(input_graph,popular_graph):
    popular_relations = []
    zero_relations = dict(map(lambda (i,n): (i,0), popular_graph))
    for (influencer,num_followers) in popular_graph:
        relation = { 'id': influencer, 'username': twitter_api.GetUser(influencer).screen_name, 'influence': num_followers, 'relations': zero_relations.copy() }
        followers = {}
        del relation['relations'][influencer]
        for (friend,user) in input_graph:
            if friend == influencer:
                followers[user] = True
        for (friend,user) in input_graph:
            if user in followers and friend in relation['relations']:
                relation['relations'][friend] += 1
        popular_relations.append(relation)
    return popular_relations

def add_user_info(popular_graph):
    user_info = {}
    rankings = [['twitter id', 'screen name', 'interlocks', 'followers', 'name', 'bio', 'location']]
    for user_list in popular_graph:
        user_info[int(user_list[0])] = { 'interlocks': int(user_list[1]) }
    user_ids = user_info.keys()
    for n in range(int(math.ceil(len(user_ids) / float(100)))):
        user_ids_batch = user_ids[n*100:(n+1)*100]
        response = twitter_api.UsersLookup(user_id=user_ids_batch)
        for user in response:
            for field in ['screen_name', 'name', 'description', 'location', 'followers_count']:
                user_info[user.id][field] = eval('user.%s' % field)
    for user_list in popular_graph:
        id = int(user_list[0])
        fields = user_info[id]
        rankings.append([id, fields['screen_name'].encode('utf-8'), int(user_list[1]), fields['followers_count'], fields['name'].encode('utf-8'), fields['description'].encode('utf-8'), fields['location'].encode('utf-8')])
    return rankings

if __name__ == '__main__':

    input_file = sys.argv[1]
    output_file = sys.argv[2]
    N = int(sys.argv[3])
    
    input_graph = reverse_list_items(get_csv(input_file))
    input_graph.sort()                            
    
    popular_graph = top_n_influential(input_graph, N)
    rankings = add_user_info(popular_graph)
    # rankings = [unicode(str(s).decode("utf-8")).encode("utf-8") for s in [t for t in ranking]]

    with open(output_file, 'wb') as f:
        writer = csv.writer(f)
        writer.writerows(rankings)

