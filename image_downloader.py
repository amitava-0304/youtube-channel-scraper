import os
import urllib.request

def download_image(url,file_name,search_term):
    file_path=r'thumbnail_images/'
    target_folder = os.path.join(file_path, '_'.join(search_term.lower().split(' ')))
    if not os.path.exists(target_folder):
        os.makedirs(target_folder)
    full_path = target_folder+'/' + str(file_name) + '.jpg'
    urllib.request.urlretrieve(url, full_path)

'''url =['https://yt3.ggpht.com/ytc/AMLnZu--BW5u0yDUi9roKCJ5iW3NSFdvxTToEMOYzXjcyw=s176-c-k-c0x00ffffff-no-rj-mo']
count=1
for i in url:
    download_image(i,count,'mysirji')
    count+=1'''
