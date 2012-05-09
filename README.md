fu-twitter-stats
================================

A Twitter Statistics Package for a project for the Freelancers Union. Graphs are powered with D3.



Influencers of An Audience
================================

1. Crawl a user's audience's followees 

For each of the people that follow <twitter_username>, the other people they follow:
python twitter-followers.py <twitter_username>

2. Create influence matrix

Find the 20 most influential people in my audience (excluding me) and a matrix
representing the interraltions between these people:
python twitter-followers.py data/<twitter_username>.csv 20 <twitter_userid>

3. Graph influence matrix

(should be served on HTTP server, not local file)
http://localhost/fu-twitter-stats/graph/influencers/?data=../../data/<twitter_username>_audience.csv.json
