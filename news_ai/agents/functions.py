from langchain_community.utilities import GoogleSerperAPIWrapper
from datetime import datetime, timedelta
import re
from news_ai.logging.logger import logging
from news_ai.exception_handler.exception import NewsException
import sys


def convert_to_datetime(relative_time):
    now = datetime.now()

    if "minute" in relative_time:
        minutes = int(re.search(r"(\d+)", relative_time).group(1))
        return now - timedelta(minutes=minutes)
    elif "hour" in relative_time:
        hours = int(re.search(r"(\d+)", relative_time).group(1))
        return now - timedelta(hours=hours)
    elif "day" in relative_time:
        days = int(re.search(r"(\d+)", relative_time).group(1))
        return now - timedelta(days=days)
    else:
        # Fallback to now if unrecognized format
        return now

def sort_news_by_date(news_list):
    return sorted(news_list, key=lambda x: convert_to_datetime(x['date']), reverse=True)

def google_news(topic: str):
    search = GoogleSerperAPIWrapper(type="news", tbs="qdr:h24")
    results = search.results(topic)
    
    for news in results["news"]:
        for key in ['imageUrl', 'position', 'snippet']:
            if key in news:
                del news[key] 

    news_list = results['news'] 
    sorted_news = sort_news_by_date(news_list)
    return sorted_news

def news(topic: str):
    logging.info("Entered in News") 
    try:
        g_news = google_news(topic)
        # r_news = get_rss_news(keyword=topic)
        # logging.info(f"r_news = {r_news}")
        # latest_news = g_news + r_news
        return g_news
    except Exception as e:
        raise NewsException(e, sys)
    
def sanitize_news_list(news_list: list[dict]) -> list[dict]:
    sanitized = []

    for item in news_list:
        try:
            if any(char in item.get("title", "") for char in ["\ufffd", "�", "ass"]):
                continue
            # Convert everything to string and filter extra fields
            news = {
                "title": str(item.get("title", "")),
                "link": str(item.get("link", "")),
                "date": str(item.get("date", "")),
                "source": str(item.get("source", ""))
            }
           
            sanitized.append(news)
        except Exception as e:
            print(f"Skipping invalid item: {item} → Error: {e}")
            continue

    return sanitized