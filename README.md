# Twitter/X Scraper using Twitkit

This project uses the `twikit` Python library to fetch tweets from specific X (formerly Twitter) user accounts. The collected tweets are used for analyzing personality traits or user behavior.

---

## 🔧 Libraries Used

| Library         | Why It's Needed |
|----------------|------------------|
| `twikit`       | Core library to fetch user info and tweets from X |
| `asyncio`      | Used to handle asynchronous tweet fetching |
| `csv`          | To write collected tweet data into structured CSV files |
| `configparser` | To safely load user credentials from `config.ini` |
| `time`         | Adds delay between requests to avoid rate-limiting |
| `datetime`     | For timestamp tracking and date filtering |
| `random`       | Adds randomized delay to mimic human behavior |

Install dependencies using:

```bash
pip install twikit
```

---

## Creating `cookies.json` (First Step)

Twikit needs authentication to access user tweets. We use cookies-based login.  
You must first create a `cookies.json` file using your X credentials.

### Steps:

1. In your `config.ini`, store:

```ini
[X]
username = YOUR_X_USERNAME
email = YOUR_X_EMAIL
password = YOUR_X_PASSWORD
```

2. In `twitkit.py`, uncomment only the **top portion**:

```python
import asyncio
from twikit import Client, TooManyRequests
...

client = Client(language='en-US')
await client.login(auth_info_1=username, auth_info_2=email, password=password)
await client.save_cookies('cookies.json')
```

3. Run the script once:
```bash
python3 twitkit.py
```

4. This creates a `cookies.json` file for all future scraping sessions.  
After this, **comment out the login code** and **uncomment `load_cookies()`** instead.

---

## Scraping Tweets

Once you have `cookies.json`, you can start scraping tweets:

```python
client.load_cookies('cookies.json')
```

Set the target user by assigning their **username** to the `QUERY` variable:
```python
QUERY = 'andrewxwilson'
```

Run the script:
```bash
python3 twitter_scraper.py
```

It fetches up to `MINIMUM_TWEETS` (default: 5000) tweets and stores them in `{QUERY}.csv`.

---

## Scraping Until a Particular Date

To limit scraping till a specific date (e.g., 2022-01-01):

1. Inside the loop, extract the tweet creation date:
```python
tweet_date = tweet.created_at_datetime
```

2. Filter:
```python
if tweet_date < datetime(2022, 1, 1, tzinfo=timezone.utc):
    break
```

---

## CSV Output Fields

Each row in the CSV contains:

- Tweet Count
- Tweet ID
- User ID
- Username
- Full Text
- Created At
- Retweets
- Likes
- Views
- In Reply To
- Media Links
- Comments
- Bookmark Count
- Location
- Hashtags
- URLs

---

## Known Limitation

> The only con of this approach is that **your account may get suspended** if too many requests are made or suspicious activity is detected.  
Use delays between requests and avoid over-scraping in a short time.


