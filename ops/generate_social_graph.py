# Import necessary libraries
import mysql.connector

# Connect to MySQL server
cnx = mysql.connector.connect(user="root", password="Admin123", host="host.minikube.internal")
cursor = cnx.cursor()

# Create social_graph database
cursor.execute("CREATE DATABASE social_graph")

# Use social_graph database
cursor.execute("USE social_graph")

# Create relationships table
create_relationships_table = """
CREATE TABLE relationships (
    id INT PRIMARY KEY AUTO_INCREMENT,
    source_id INT NOT NULL,
    destination_id INT NOT NULL,
    INDEX (destination_id)
)
"""
cursor.execute(create_relationships_table)

# Get users from twitter database
cursor.execute("USE twitter")
get_users = """
SELECT id FROM users
"""
cursor.execute(get_users)
users = cursor.fetchall()

# Use social_graph database
cursor.execute("USE social_graph")

# Insert relationships into relationships table
add_relationship = """
INSERT INTO relationships (source_id, destination_id) VALUES (%s, %s)
"""
for user in users:
    for other_user in users:
        if user[0] != other_user[0]:
            cursor.execute(add_relationship, (user[0], other_user[0]))
cnx.commit()
