
## Generate init script for write-api
```
write me an init script for a mysql database that includes
a user table and a tweet table. The user table should have
the columns id, which should be the primary key, and username.

The tweet table should have the columns id as primary key, body,
and user_id where user_id is a foreign key that references the
id column from the user table. The database should be named twitter.

All fields cannot be null.
```

## Generate write-api
```
write me a python service that is an API with 1 POST endpoint
that receives a tweet for a specific user, checks if that user
exists in the user table and if the user does exist, inserts
the tweet into the tweet table. All request fields should be
validated and not null.

After the tweet is inserted into the tweet table, the tweet
data should be added as a message onto a rabbitmq queue to
later be consumed by a downstream service.
```

## Generate init script for social graph
```
write me an init script for a mysql database called social_graph
that includes a table called relationship. The table should have
the columns id which is the primary key, destination_id, and
user_id. All column types should be INT. The column destination_id
should be indexed.
```

## Generate social graph service 
```
write me a python service that is an API with 1 GET endpoint
that has a request param tweeter_id. It should then take that
tweeter_id and query the before mentioned relationship table
of the social_graph database where tweeter_id is equal to
destination_id. It should then return all of the source_ids from
the results of the query and return them to the client.
```

## Generate fanout service
```
write me a python consumer service that consumes a message
from a rabbit mq queue. The message that is consumed will contain
the fields user_id, tweet_id, body. The user_id should first
be used as the tweeter_id request param to send a get request to the social
graph service that I asked you to create for me. For every source_id in the list returned
from that service, you should search for that
key in redis. The structure in redis will be HSET user_id "list".
If the key exists you should append a new object to the list
with the key tweet_id where the value is the tweet_id from the
rabbitmq message and the key user_id where the user_id is the one from
the rabbit mq message. The write to redis should use optimistic
locking to prevent race conditions. If the list pointed to by the
key has a length equal to 800, you should remove the 0th index element
in the list before adding the new one.

After this you should create a new object in memcached where
the tweet_id from the rabbitmq message is the key and the body
from the rabbitmq message is the body.

Make sure the service has some sort of graceful shutdown implementation.
```

## Generate read-api
```
Can you write me a python api that will take a user_id as a param and then search for that 
users_ids home timeline in the redis we created. Then for every tweet object in that users 
home timeline, search for the tweet body in the memcached using the tweet_id from the home 
timeline. Then the api should return a list of {tweet_body, username} where username is the 
user that created that tweet?
```
