import feedparser
from config import RSS_URL
from datetime import datetime,timedelta
from dateutil import parser



def get_timed_digest(categories,time):
    feed = feedparser.parse(RSS_URL)

    now = datetime.now()
    one_day_ago = datetime(now.year, now.month, now.day, int(time[:2]), int(time[3:]))- timedelta(days=1)
    digest = []
    for post in feed.entries:
         news = dict()
         if post.tags[0].term in categories and one_day_ago < parser.parse(post['published']).replace(tzinfo=None):
            news['title'] = post.title
            news['link'] = post.link
            digest.append(news)

    return digest

def get_immediately_digest():
    feed = feedparser.parse(RSS_URL)

    now = datetime.now()
    one_day_ago = datetime(now.year, now.month, now.day, now.hour, now.minute)- timedelta(days=1)
    digest = []
    for post in feed.entries:
         news = dict()
         if one_day_ago < parser.parse(post['published']).replace(tzinfo=None):
            news['title'] = post.title
            news['link'] = post.link
            digest.append(news)

    return digest


