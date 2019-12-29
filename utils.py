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


import json
from collections import Counter

def getuserdata():
    with open('data.json') as json_file:
        data = json.load(json_file)
    return data

def save_and_update_data(userdata:dict):
    try:
        with open('data.json') as f:
            data = json.load(f)
            f.close()
    except Exception:
            with open('data.json','w') as f:
                data = []
                json.dump(data, f)
                f.close()
    categories = []
    for item in userdata['categories']:
        categories.append(item)
    userdata['categories'] = categories
    data.append(userdata)
    with open('data.json', 'w') as f:
        print(data)
        json.dump(data, f)
        f.close()


def show_statistics():

    with open('data.json') as f:
        data = json.load(f)
        f.close()
    users_count = len(data)

    categories = []
    times = []
    for item in data:   
        times.append(item['time'])
        for cat in item['categories']:
            categories.append(cat)
    

    categories_str = ""

    for k,v in Counter(categories).most_common(100):
        
        categories_str+="{}: {}\n".format(k,v)

    
    times_str = ""

    for k,v in Counter(times).most_common(100):
        
        times_str+="{}: {}\n".format(k,v)


    return """Кількість підписок: {}\n\nПідписка на категорії у розрізі популярності:\n{}\nБажаний час дайджесту:\n{}""".format(users_count, categories_str, times_str)

import pickle

def save_intercations(data):
    try:
        import cPickle as pickle
    except ImportError:  # python 3.x
        import pickle

    with open('data.p', 'wb') as fp:
        pickle.dump(data, fp)

def load_interaction():
    with open('data.p', 'rb') as fp:
        data = pickle.load(fp)
    return data

