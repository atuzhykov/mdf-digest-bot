import os
from sqlalchemy import create_engine
from collections import Counter

# DATABASE_URL = os.environ['DATABASE_URL']
DATABASE_URL = "postgres://djjjggumxrnpvv:4674906ce612a3808d5f66b1231c32c86c475d00f8feeab78d161b37afb45310@ec2-107-22-234-204.compute-1.amazonaws.com:5432/d81vc88eqc015v"

engine = create_engine(DATABASE_URL)

from sqlalchemy import Table, Column, Integer, String, MetaData
meta = MetaData()

users = Table(
   'users', meta, 
   Column('chat_id', Integer, primary_key = True), 
   Column('name', String), 
   Column('categories', String), 
   Column('time', String), 
)

# meta.create_all(engine)

# conn = engine.connect()




def save_to_db(chat_id, user_name, categories, time):
    DATABASE_URL = "postgres://djjjggumxrnpvv:4674906ce612a3808d5f66b1231c32c86c475d00f8feeab78d161b37afb45310@ec2-107-22-234-204.compute-1.amazonaws.com:5432/d81vc88eqc015v"
    engine = create_engine(DATABASE_URL)
    conn = engine.connect()
    ins = users.insert().values(chat_id = chat_id, name = user_name,categories = categories, time=time)
    result = conn.execute(ins)

def load_from_db():
    DATABASE_URL = "postgres://djjjggumxrnpvv:4674906ce612a3808d5f66b1231c32c86c475d00f8feeab78d161b37afb45310@ec2-107-22-234-204.compute-1.amazonaws.com:5432/d81vc88eqc015v"
    engine = create_engine(DATABASE_URL)
    conn = engine.connect()
    s = users.select()
    return conn.execute(s)

def load_from_db_by_chat_id(chat_id):
    DATABASE_URL = "postgres://djjjggumxrnpvv:4674906ce612a3808d5f66b1231c32c86c475d00f8feeab78d161b37afb45310@ec2-107-22-234-204.compute-1.amazonaws.com:5432/d81vc88eqc015v"
    engine = create_engine(DATABASE_URL)
    conn = engine.connect()
    user = users.select().where(users.c.chat_id == chat_id)
    return conn.execute(user).fetchall()

def update_by(chat_id, categories, time):
    DATABASE_URL = "postgres://djjjggumxrnpvv:4674906ce612a3808d5f66b1231c32c86c475d00f8feeab78d161b37afb45310@ec2-107-22-234-204.compute-1.amazonaws.com:5432/d81vc88eqc015v"
    engine = create_engine(DATABASE_URL)
    conn = engine.connect()
    user = users.update().\
            where(users.c.chat_id==chat_id).\
            values(categories=categories, time = time)
    conn.execute(user)

def statistics():
    DATABASE_URL = "postgres://djjjggumxrnpvv:4674906ce612a3808d5f66b1231c32c86c475d00f8feeab78d161b37afb45310@ec2-107-22-234-204.compute-1.amazonaws.com:5432/d81vc88eqc015v"
    engine = create_engine(DATABASE_URL)
    conn = engine.connect()
    data = conn.execute(users.select()).fetchall()
    users_count = len(data)
    print(users_count)

    categories = []
    times = []
    for item in data:   
        times.append(item[3])
        cats = item[2].strip('{ }').replace('"', '').replace(' ', '').split(',')
        for cat in cats:
            categories.append(cat)
    

    categories_str = ""

    for k,v in Counter(categories).most_common(100):
        
        categories_str+="{}: {}\n".format(k,v)

    
    times_str = ""

    for k,v in Counter(times).most_common(100):
        
        times_str+="{}: {}\n".format(k,v)


    return """Кількість підписок: {}\n\nПідписка на категорії у розрізі популярності:\n{}\nБажаний час дайджесту:\n{}""".format(users_count, categories_str, times_str)


print(statistics())












