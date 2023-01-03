import pika
import mysql.connector
import redis
import memcache
import requests
import json

# Connect to the Redis server
r = redis.Redis(host="redis", port=6379, db=0)

# Connect to the Memcached server
mc = memcache.Client(["memcached:11211"])

# Set up a connection to the RabbitMQ server
connection = pika.BlockingConnection(pika.ConnectionParameters("rabbit"))
channel = connection.channel()

# Set up a connection to the social graph service
SOCIAL_GRAPH_URL = "http://social-graph:5000/relationships"


def callback(ch, method, properties, body):
    # Parse the message
    message = json.loads(body)
    user_id = message["user_id"]
    tweet_id = message["id"]
    tweet_body = message["body"]

    # Query the social graph service for a list of source_ids
    params = {"tweeter_id": user_id}
    response = requests.get(SOCIAL_GRAPH_URL, params=params)
    source_ids = response.json()["source_ids"]

    # Write the tweet data to Redis and Memcached
    for source_id in source_ids:
        key = f"{source_id}:tweets"

        # Use optimistic locking to prevent race conditions
        while True:
            try:
                # Check if the key already exists in Redis
                if r.exists(key):
                    # If the list is already 800 items long, remove the first item
                    if r.llen(key) == 800:
                        r.lpop(key)
                    # Append the new tweet and user_id to the list
                    r.rpush(key, {"tweet_id": tweet_id, "user_id": user_id})
                else:
                    # If the key does not exist, create a new list with the tweet and user_id
                    r.rpush(key, {"tweet_id": tweet_id, "user_id": user_id})
                break
            except redis.WatchError:
                continue

        # Write the tweet body to Memcached
        mc.set(tweet_id, tweet_body)


# Set up a consumer to consume messages from the queue
channel.basic_consume(callback, queue="tweet", no_ack=True)

# Graceful shutdown implementation
def shutdown():
    # Close the RabbitMQ connection
    connection.close()


# Set up a signal handler to catch SIGINT and SIGTERM signals
def sigint_handler(signum, frame):
    shutdown()


import signal

signal.signal(signal.SIGINT, sigint_handler)
signal.signal(signal.SIGTERM, sigint_handler)

# Start consuming messages
print("[*] Waiting for messages. To exit press CTRL+C")
channel.start_consuming()
