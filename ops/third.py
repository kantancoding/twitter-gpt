# Import necessary libraries
import mysql.connector
import redis
import pymemcache

# Connect to MySQL, Redis, and Memcached servers
mysql_cnx = mysql.connector.connect(
    user="root", password="admin123", host="localhost"
)
mysql_cursor = mysql_cnx.cursor()
redis_cnx = redis.Redis(host="localhost", port=6379)
memcached_cnx = pymemcache.client.base.Client(("localhost", 11211))

# Use twitter database
mysql_cursor.execute("USE twitter")

# Get users from twitter database
get_users = """
SELECT id FROM users
"""
mysql_cursor.execute(get_users)
users = mysql_cursor.fetchall()

# Get tweets from twitter database
get_tweets = """
SELECT id, user_id, body FROM tweets
"""
mysql_cursor.execute(get_tweets)
tweets = mysql_cursor.fetchall()

# Insert tweets into Redis and Memcached for each user
for user in users:
    key = f"{user[0]}:home_timeline"
    timeline = []
    for other_user in users:
        if other_user[0] != user[0]:  # Check if other user is not the current user
            # Find first tweet from other user
            for tweet in tweets:
                if tweet[1] == other_user[0]:
                    timeline.append({"tweet_id": tweet[0], "user_id": tweet[1]})
                    # Insert tweet into Memcached
                    tweet_key = tweet[0]
                    tweet_value = tweet[2]
                    memcached_cnx.set(tweet_key, tweet_value)
                    break  # Add only one tweet from each user
    redis_cnx.rpush(key, timeline)
