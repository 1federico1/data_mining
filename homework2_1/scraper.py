import requests as r
from bs4 import BeautifulSoup
import os
import time
import re
from random import randint

page = 'https://www.kijiji.it/offerte-di-lavoro/offerta/informatica-e-web'

if os.path.isfile('jobs.tsv'):
    os.remove('jobs.tsv')

url = r.get(page)
soup = BeautifulSoup(url.text, 'html.parser')

num_pages = int(soup.find(class_='last-page', text=True).contents[0])
count = 1

while count <= num_pages:

    new_url = url.url + "?p=" + str(count)
    current_page = r.get(new_url)
    print(current_page.url)

    tmp_soup = BeautifulSoup(current_page.text, 'html.parser')
    ann_list = tmp_soup.find_all(class_='item-content')

    links = []
    titles = []
    descriptions = []
    locations = []
    timestamps = []
    full_descriptions = []

    for elem in ann_list:
        item = elem.find(class_='cta', href=True, text=True)
        links.append(item['href'])
        titles.append(re.sub('\s+', ' ', item.contents[0].strip()))

        description_item = elem.find(class_='description', text=True)
        descriptions.append(re.sub('\s+', ' ', description_item.contents[0]))

        location_item = elem.find(class_='locale', text=True)
        locations.append(location_item.contents[0])

        timestamp_item = elem.find(class_='timestamp', text=True)
        timestamps.append(timestamp_item.contents[0])

    with open('jobs.tsv', 'a') as tsv_file:
        for i in range(num_pages-1):
            try:
                row = titles[i] + '\t' + descriptions[i] + '\t' + locations[i] + '\t' + timestamps[i] + '\t' + \
                      links[i] + '\n'
            except IndexError:
                continue
            tsv_file.write(str(row))
    sleep_time = randint(1, 5)
    time.sleep(sleep_time)

    count += 1
