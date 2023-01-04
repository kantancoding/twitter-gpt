# This script creates two tables in the twitter database: users and tweets.
# It then inserts some user records and tweet records into the respective tables.
import mysql.connector
import random

# Connect to the database
cnx = mysql.connector.connect(
    user="root", password="Admin123", host="localhost"
)
cursor = cnx.cursor()

# Create twitter database
cursor.execute("CREATE DATABASE twitter")

# Use twitter database
cursor.execute("USE twitter")

create_users_table = """
CREATE TABLE users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(255) UNIQUE NOT NULL
)
"""
cursor.execute(create_users_table)

# Create the tweets table
create_tweets_table = """
CREATE TABLE tweets (
  id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
  body VARCHAR(255) NOT NULL,
  user_id INT NOT NULL,
  FOREIGN KEY (user_id) REFERENCES users(id)
);
"""
cursor.execute(create_tweets_table)

# Insert 100 users
users = [
    ("Alice"),
    ("Bob"),
    ("Charlie"),
    ("Dave"),
    ("Eve"),
    ("Frank"),
    ("Grace"),
    ("Heather"),
    ("Igor"),
    ("Jenny"),
    ("Karen"),
    ("Larry"),
    ("Maggie"),
    ("Nancy"),
    ("Owen"),
    ("Patty"),
    ("Quincy"),
    ("Randy"),
    ("Stephanie"),
    ("Tina"),
    ("Ursula"),
    ("Vicky"),
    ("Wendy"),
    ("Xavier"),
    ("Yolanda"),
    ("Zach"),
    ("Avery"),
    ("Brett"),
    ("Carla"),
    ("Derek"),
    ("Emma"),
    ("Flynn"),
    ("Greta"),
    ("Holly"),
    ("Ira"),
    ("Jasmine"),
    ("Katie"),
    ("Leo"),
    ("Maddie"),
    ("Nate"),
    ("Olivia"),
    ("Patrick"),
    ("Quinn"),
    ("Roxanne"),
    ("Sam"),
    ("Tessa"),
    ("Uma"),
    ("Victor"),
    ("Wendy"),
    ("Xander"),
    ("Yvette"),
    ("Zane"),
    ("Abby"),
    ("Becca"),
    ("Chad"),
    ("Dawn"),
    ("Eli"),
    ("Fiona"),
    ("Gus"),
    ("Hannah"),
    ("Ian"),
    ("Jill"),
    ("Kara"),
    ("Liam"),
    ("Mia"),
    ("Nina"),
    ("Oscar"),
    ("Pam"),
    ("Quincy"),
    ("Rory"),
    ("Sally"),
    ("Tara"),
    ("Ursula"),
    ("Violet"),
    ("Will"),
    ("Xena"),
    ("Yara"),
    ("Zelda"),
]
add_user = """
INSERT INTO users (username) VALUES (%s)
"""
cursor.executemany(add_user, users)

# Generate tweets for each user
tweet_bodies = [
    "Just setting up my Twitter",
    "I love Python",
    "My favorite color is blue",
    "Exploring MySQL",
    "Experimenting with Docker",
    "Discovering Kubernetes",
    "Playing with RabbitMQ",
    "Trying out Redis",
    "Using Memcached",
    "I love solving programming challenges",
    "Dabbling in machine learning",
    "Studying natural language processing",
    "Data analysis is interesting",
    "Web development is fun",
    "Cloud computing is cool",
    "Learning about devops",
    "Interested in computer science",
    "Software engineering is fascinating",
    "Learning about software design patterns",
    "Algorithms and data structures are my jam",
    "Databases are intriguing",
    "Networking is intriguing",
    "Security is important",
    "Artificial intelligence is amazing",
    "Cybersecurity is crucial",
    "Blockchain is interesting",
    "Distributed systems are complex",
    "Mobile development is convenient",
    "Game development is exciting",
    "Virtual reality is immersive",
    "Augmented reality is cool",
]

for user in users:
    num_tweets = random.randint(1, 10)
    for i in range(num_tweets):
        tweet_body = random.choice(tweet_bodies)
        add_tweet = """
        INSERT INTO tweets (user_id, body)
        VALUES (%s, %s)
        """
        user_id = cursor.execute(
            """
        SELECT id FROM users WHERE username = %s
        """,
            (user,),
        )
        cursor.execute(add_tweet, (user_id, tweet_body))

# Commit the transaction
cnx.commit()

# Close the connection
cnx.close()
