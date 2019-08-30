def divide_chunks(l, n): 
      
    # looping till length l 
    for i in range(0, len(l), n):  
        yield l[i:i + n]

import feedparser
def get_all_tags(RSS_URL):
    feed = feedparser.parse(RSS_URL)
    tags = []
    for post in feed.entries:
        tags.append(post.tags[0].term)
    return set(tags)