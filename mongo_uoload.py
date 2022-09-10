'''import glob
from skimage import io
from pymongo import MongoClient
import pymongo
import gridfs
file_list = glob.glob(r'thumbnail_images\*.jpg')
print(file_list)
client = pymongo.MongoClient("mongodb+srv://amitava_2112:Suman123@python.e0zfy.mongodb.net/?retryWrites=true&w=majority")
db = client.test
database = client['thumbnail_images']
#Create a object of GridFs for the above database.
fs = gridfs.GridFS(database)
#define an image object with the location.

for i in file_list:
    with open(i, 'rb') as f:
        contents = f.read()
#Now store/put the image via GridFs object.
    fs.put(contents, filename="file")'''

from pymongo import MongoClient
from PIL import Image
import io
import glob
client = MongoClient("mongodb+srv://amitava_2112:Suman123@python.e0zfy.mongodb.net/?retryWrites=true&w=majority")
db = client.Youtuber
images = db.thumbnil_images
file_list = glob.glob(r'thumbnail_images\*.jpg')
for i in file_list:
    im = Image.open(i)
    image_bytes = io.BytesIO()
    im.save(image_bytes, format='JPEG')

    image = {
    'data': image_bytes.getvalue()
     }

    image_id = images.insert_one(image).inserted_id
