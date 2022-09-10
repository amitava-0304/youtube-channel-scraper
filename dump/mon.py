import pymongo
client = pymongo.MongoClient("mongodb+srv://amitava_2112:Suman123@python.e0zfy.mongodb.net/?retryWrites=true&w=majority")
db = client.test
database = client['Internship']
collection = database["data1"]
data = {
    "pcode": 101,
    "tech": 'tech',
    "project": 'project',
    "domain": 'domain'
}
collection.insert_one(data)