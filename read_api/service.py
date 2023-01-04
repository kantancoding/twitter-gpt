import flask
import redis
import json
import pymemcache

# Connect to Redis and Memcached servers
redis_cnx = redis.Redis(host="redis", port=6379)
memcached_cnx = pymemcache.client.base.Client(("memcached", 11211))

app = flask.Flask(__name__)


@app.route("/home_timeline", methods=["GET"])
def home_timeline():
    # Get user_id parameter from request
    user_id = flask.request.args.get("user_id")

    # Get home timeline from Redis
    key = f"{user_id}:home_timeline"
    string_list = redis_cnx.lrange(key, 0, -1)
    timeline = [json.loads(s) for s in string_list]

    # Get tweet data from Memcached and build response list
    tweets = []
    for tweet in timeline:
        tweet_id = tweet["tweet_id"]
        tweet_body = memcached_cnx.get(tweet_id)
        user_id = tweet["user_id"]
        tweets.append({"tweet_body": tweet_body, "user_id": user_id})

    response = flask.jsonify(tweets)
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8080)
