import feedparser
from datetime import datetime, timedelta, timezone
import requests
# RSS feeds organized by type
rss_feeds = {
    "Top Stories": [
        "https://www.cbc.ca/cmlink/rss-topstories",
        "https://www.thestar.com/search/?f=rss&t=article&bl=2827101&l=20",
        "https://globalnews.ca/feed/",
        "https://nationalpost.com/feed/",
    ],
    "World News": [
        "https://www.cbc.ca/cmlink/rss-world",
        "https://globalnews.ca/world/feed/",
        "http://rss.cnn.com/rss/edition_world.rss"
    ],
    "Canada News": [
        "https://www.cbc.ca/cmlink/rss-canada",
        "https://globalnews.ca/canada/feed/"
    ]
}

now = datetime.now(timezone.utc)
last_24hrs = now - timedelta(days=1)


def news():
    rss_feeds_news = []
    for urls in rss_feeds.values():
            for url in urls:
                try:
                    # Fetch RSS with timeout
                    response = requests.get(url, timeout=5)
                    feed = feedparser.parse(response.content)

                    for entry in feed.entries:
                        # print(entry)
                        try:
                            published_time = datetime(*entry.published_parsed[:6])
                            published_time = published_time.replace(tzinfo=timezone.utc)
                            # print(published_time)
                            if published_time > last_24hrs:
                                # print(entry.title)
                                news_item = {
                                    "title": entry.title,
                                    "link": entry.link,
                                    "date": published_time.strftime('%Y-%m-%d %H:%M:%S'), #todo
                                    "source": feed.feed.get("title", "Unknown Source"), #todo
                                }
                                rss_feeds_news.append(news_item)
                        except Exception as e:
                            print(f"⚠️ Entry error: {e}")
                            continue

                except requests.exceptions.Timeout:
                    print(f"⏰ Timeout: {url}")
                except Exception as e:
                    print(f"❌ Failed to fetch {url}: {e}")

    return rss_feeds_news
