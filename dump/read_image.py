from pymongo import MongoClient
from bson.binary import Binary
from PIL import Image
import io
import matplotlib.pyplot as plt

client = MongoClient('mongodb+srv://amitava_2112:Suman123@python.e0zfy.mongodb.net/?retryWrites=true&w=majority')
db = client.testdb
images = db.images
#image = images.find_one()
for x in images.find():
  print(x)
  pil_img = Image.open(io.BytesIO(x['data']))
  plt.imshow(pil_img)
  plt.show()