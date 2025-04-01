from news_ai.db.db import init_db, insert_news, delete_old_news
from news_ai.db.rss_feed import rss_news

init_db()

news_list = rss_news()

insert_news(news_list=news_list)

delete_old_news()

