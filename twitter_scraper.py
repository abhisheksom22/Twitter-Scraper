import asyncio
from twikit import Client, TooManyRequests  # Main library to interact with X (Twitter)
import time
from datetime import datetime  # For logging timestamps
import csv  # To store output data
from configparser import ConfigParser  # To read credentials from config.ini
from random import randint  # Adds delay randomness to avoid detection

# Set how many tweets you want to collect
MINIMUM_TWEETS = 5000

# X (Twitter) username to scrape (without @)
QUERY = 'andrewxwilson'


# Async function to get tweets (either first batch or paginated next batch)
async def get_tweets(tweets):
    if tweets is None:
        print(f'{datetime.now()} - Getting tweets...')
        user = await client.get_user_by_screen_name(QUERY)  # get user details
        user_id = user.id
        tweets = await client.get_user_tweets(user_id, 'Tweets', 20)  # get user's tweets
    else:
        wait_time = randint(5, 10)  # random delay to reduce chances of suspension
        print(f'{datetime.now()} - Getting next tweets after {wait_time} seconds ...')
        time.sleep(wait_time)
        tweets = await tweets.next()  # go to next tweet page

    return tweets


# Main async function to initialize and run the scraper
async def main():
    global client

    # Load credentials from config file
    config = ConfigParser()
    config.read('config.ini')
    username = config['X']['username']
    email = config['X']['email']
    password = config['X']['password']

    # Initialize Twikit client
    client = Client(language='en-US')

    # Uncomment this block only ONCE to create cookies.json for login
    # await client.login(auth_info_1=username, auth_info_2=email, password=password)
    # await client.save_cookies('cookies.json')
    print("cookie json created")

    # Load cookies for session reuse (safer and faster)
    client.load_cookies('cookies.json')

    tweet_count = 0
    tweets = None

    # Create a new CSV to store scraped tweets
    with open(f'{QUERY}.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([
            'Tweet_count', 'Tweet ID', 'UserId', 'Username', 'Text', 'Created At',
            'Retweets', 'Likes', 'Views', 'In Reply To', 'Media Links',
            'Comments', 'Bookmark Count', 'Location', 'Hashtags', 'urls'
        ])

    # Loop until required number of tweets is scraped
    while tweet_count < MINIMUM_TWEETS:
        try:
            tweets = await get_tweets(tweets)
        except TooManyRequests as e:
            # If rate-limited, wait until limit resets
            rate_limit_reset = datetime.fromtimestamp(e.rate_limit_reset)
            print(f'{datetime.now()} - Rate limit reached. Waiting until {rate_limit_reset}')
            wait_time = rate_limit_reset - datetime.now()
            time.sleep(wait_time.total_seconds())
            continue

        # Break if no tweets are returned
        if not tweets:
            print(f'{datetime.now()} - No more tweets found')
            break

        # Loop over each tweet and write to CSV
        for tweet in tweets:
            tweet_count += 1
            tweet_data = [
                tweet_count,
                tweet.id,
                tweet.user.id,
                tweet.user.screen_name,
                tweet.full_text,
                tweet.created_at_datetime,
                tweet.retweet_count,
                tweet.favorite_count,
                tweet.view_count,
                tweet.in_reply_to,
                tweet.media,
                tweet.reply_count,
                tweet.bookmark_count,
                tweet.place,
                tweet.hashtags,
                tweet.urls
            ]

            # Append each tweet to the CSV file
            with open(f'{QUERY}.csv', 'a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(tweet_data)

        print(f'{datetime.now()} - Got {tweet_count} tweets')

    print(f'{datetime.now()} - Done! Got {tweet_count} tweets found')


# Run the async main function
if __name__ == '__main__':
    asyncio.run(main())
