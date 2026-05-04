import tweepy

bearer_token = "AAAAAAAAAAAAAAAAAAAAAMxw9QEAAAAAn7PySqkhk9DkbYgHyp77ezg9pvQ%3DWvu3MFU8uAr8L3VWVZQh36qGPSEnwJRPMhL4fx9IwuZ4H7lp9g"

client = tweepy.Client(bearer_token=bearer_token)

query = "#lpgcrisis lang:en -is:retweet"

response = client.search_recent_tweets(
    query=query,
    max_results=10,
    tweet_fields=["created_at", "text"]
)

if response.data:
    for tweet in response.data:
        print(tweet.text)
else:
    print("No tweets found")