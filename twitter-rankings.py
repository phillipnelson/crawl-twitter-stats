'''
Rank the top N influencers in graph

Usage:  python twitter-rankings.py <audience_graph_file>.txt [N=20] [skip_user=<username>]

Input:
    File of audience graph: (user1) follows (user2)
    Format:     <user_id>,<friend_id>

Output: 
    File:       <username>_graph.json
    Format:     [??]

'''

import json
import sys

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
        if skip_user and skip_user == friend:
            continue
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

if __name__ == '__main__':

    input_file = sys.argv[1]
    N = int(sys.argv[2])
    skip_user = sys.argv[3] if len(sys.argv) == 4 else False
    
    input_graph = reverse_list_items(get_csv(input_file))
    input_graph.sort()                            
    
    popular_graph = top_n_influential(input_graph, N)
    popular_matrix = top_n_relations(input_graph,popular_graph)
    
    print json.dumps(popular_graph,indent=2)
    print json.dumps(popular_matrix,indent=2)
    
    popular_matrix_file  = open('%s.json' % input_file, 'w')
    popular_matrix_file.write(json.dumps(popular_matrix))
    popular_matrix_file.close()
