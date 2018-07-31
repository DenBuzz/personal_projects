from lxml import html
import requests
from io import BytesIO
from PIL import Image
import imageio
import numpy as np

search = 'arvada'
text = search.replace(' ', '+')
query = 'http://www.cleardarksky.com/cgi-bin/find_chart.py?keys=' + text + '&type=text&Mn=astronomy&doit=Find'
result = html.fromstring(requests.get(query).content).xpath('//td[2]/a/@href')[0].replace('..','')

base_url = 'http://www.cleardarksky.com/'

page = requests.get(base_url + result)
tree = html.fromstring(page.content)
img_link = tree.xpath('//img[@id="csk_image"]/@src')[0]
main_img = Image.open(BytesIO(requests.get(base_url+img_link).content))
main_img.show()

cloud_links = [base_url + link[3:] for link in tree.xpath('//map/area/@href')[:46]]
cloud_images = []
for link in cloud_links:
    page = requests.get(link)
    tree = html.fromstring(page.content)
    background = tree.xpath('//table[@name="mapimage"]/@background')[0]
    cloud_images.append(imageio.imread(BytesIO(requests.get(background).content)))

gif_images = np.array(cloud_images)

mimsave('~/Documents/python/personal/personal_projects/cloud_movie.gif', gif_images, duration=0.15)
