fu-twitter-stats
================================

A Twitter Statistics Package for a project for the Freelancers Union. Graphs are powered with D3.


General Setup
================================

1. Create a list of Twitter OAUTH credentials @ config/twitter.py 

This is our attempt to crawl at full (single threaded) speed indefinitely. 
Try to get about 20, 30 credentials in there.


Influencers of An Audience
================================

1. Crawl a user's audience's followees 

For each of the people that follow <twitter_username>, the other people they follow:

python twitter-followers.py <twitter_username>

2. Create influence matrix

Find the 20 most influential people in the audience of <twitter_username> (excluding 
<twitter_username>) and a matrix representing the interrelations between these people:

python twitter-rankings.py data/<twitter_username>.csv 20 <twitter_username>

3. Graph influence matrix

This should be served on HTTP server, not local file, due to XSS:

http://localhost/fu-twitter-stats/graph/influencers/?data=../../data/<twitter_username>_audience.csv.json
