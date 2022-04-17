
import json
from pymongo import MongoClient 

myclient = MongoClient("mongodb://localhost:27017/") 
count = 1
db = myclient["291db"]
   



def load_json(file_name, collection_name):
    global myclient, db, count
   # name_basics, title_basics, title_principals and title_ratings
    myclient.drop_database(collection_name)
    print("creating collection {}......".format(count))
    count += 1
    Collection = db[collection_name]
    with open(file_name) as file:
        file_data = json.load(file)
      
    if isinstance(file_data, list):
        Collection.insert_many(file_data)  
    else:
        Collection.insert_one(file_data)


load_json("name.basics.json","name_basics")
load_json("title.basics.json", "title_basics")
load_json("title.principals.json", "title_principals")
load_json("title.ratings.json", "title_ratings")


# open_name = open(""
# open_titleB = ""
# open_titleP = ""
# open_titleR = ""