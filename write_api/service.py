import pika, json
import mysql.connector
from flask import Flask, request

# Connect to the MySQL database
db = mysql.connector.connect(
  host="localhost",
  user="root",
  password="admin123",
  database="twitter"
)

# Create a new Flask app
app = Flask(__name__)

# Connect to the RabbitMQ server
connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
channel = connection.channel()

# Declare the queue
channel.queue_declare(queue='tweet')

@app.route('/tweet', methods=['POST'])
def insert_tweet():
  # Validate the request fields
  if 'username' not in request.form or 'tweet' not in request.form:
    return 'Missing required fields', 400

  username = request.form['username']
  tweet_body = request.form['tweet']

  # Check if the user exists in the database
  cursor = db.cursor()
  cursor.execute("SELECT * FROM user WHERE username = %s", (username,))
  user = cursor.fetchone()
  if not user:
    return 'User does not exist', 400

  # Insert the tweet into the database
  user_id = user[0]
  cursor.execute("INSERT INTO tweet (body, user_id) VALUES (%s, %s)", (tweet_body, user_id))
  db.commit()
  tweet_id = cursor.lastrowid

  # Add the tweet data to the RabbitMQ queue
  message = {
    'id': tweet_id,
    'user_id': user_id,
    'body': tweet_body
  }
  channel.basic_publish(exchange='', routing_key='tweet', body=json.dumps(message))

  return 'Tweet added successfully', 201

if __name__ == '__main__':
  app.run(port=8080)

