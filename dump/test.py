from urllib import request

import pymongo
from flask import render_template

searchTitle = input()
try:

    client = pymongo.MongoClient(
        "mongodb+srv://amitava_2112:Suman123@python.e0zfy.mongodb.net/?retryWrites=true&w=majority")
    db = client.test
    print(db)
    database = client['Youtuber']
    print(database)
    collection = database["reviews"]
    print(collection)
    # collection.insert_many(data)
    title=collection.find({'Title':searchTitle})
    print(title)
    l=[]
    for i in title:
        l.append(i)
    for i in l:
        print(i['Commenter'])

except:
            print('something is wrong')
