import requests
from bs4 import BeautifulSoup
import urllib.error
import re
from io import BytesIO
from PIL import Image
import numpy as np

TARGET  = 'http://www.maruchou-koubeya.jp/leaflet/'
WEEK    = {'Sunday'     :[1336,205,1977,1088],
           'Monday'     :[1976,205,2300,1088],
           'Tuesday'    :[50,205,379,1088],
           'Wednesday'  :[372,205,700,1088],
           'Thursday'   :[696,205,1021,1008],
           'Friday'     :[1022,205,1339,1088],
           'Saturday'   :[1336,205,1977,1088]}
KEYWORD = 'ラスパ白山'
LEAFLET = "leaflet.jpeg"

def download_leaflet(url,keyword,path):
    imgurl = get_leaflet_url(url,keyword)
    print(imgurl)
    r = requests.get(imgurl)
    if r.status_code == 200:
        i = Image.open(BytesIO(r.content))
        imgname = f"leaflet.{i.format.lower()}"
        save_image(i,imgname)
        return imgname

def get_leaflet_url(url,keyword):
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "html.parser")
    for i in soup.find_all(['tr']):
        if keyword in i.text:
            return i.find('a').get('href')

def save_image(image,path):
    image.save(path)

def load_image(path):
    return Image.open('./'+path)

def scale_to_height(img, height):
    width = round(img.width * height / img.height)
    return img.resize((width, height))

leafret_path = download_leaflet(TARGET,KEYWORD,LEAFLET)
img = load_image(leafret_path)

for k, v in WEEK.items():
    print(k,v)
    img_crop = img.crop(v)
    img_resize = scale_to_height(img_crop, 300)
    save_image(img_resize, f"tokubai_{k}.png")



# for i in soup.find_all(['tr']):
#     if "ラスパ白山" in i.text:
#         imgurl = i.find('a').get('href')

# r = requests.get(imgurl)


# save_image(r.content, file_name)


