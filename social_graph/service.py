import mysql.connector
from flask import Flask, request

# Connect to the MySQL database
db = mysql.connector.connect(
  host="localhost",
  user="root",
  password="admin123",
  database="social_graph"
)

# Create a new Flask app
app = Flask(__name__)

@app.route('/relationships', methods=['GET'])
def get_relationships():
  # Validate the request parameter
  if 'tweeter_id' not in request.args:
    return 'Missing required parameter', 400

  tweeter_id = request.args['tweeter_id']

  # Query the relationship table
  cursor = db.cursor()
  cursor.execute("SELECT source_id FROM relationship WHERE destination_id = %s", (tweeter_id,))
  rows = cursor.fetchall()

  # Extract the source_ids from the query results
  source_ids = [row[0] for row in rows]

  return {'source_ids': source_ids}, 200

if __name__ == '__main__':
  app.run(port=8080)

