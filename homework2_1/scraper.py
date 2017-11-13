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

links = []
titles = []
descriptions = []
locations = []
timestamps = []
full_descriptions = []

while count <= num_pages:

    new_url = url.url + "?p=" + str(count)
    current_page = r.get(new_url)
    print('scraping ' + current_page.url + ' for announcements')

    tmp_soup = BeautifulSoup(current_page.text, 'html.parser')
    ann_list = tmp_soup.find_all(class_='item-content')

    for elem in ann_list:
        item = elem.find(class_='cta', href=True, text=True)
        ann_url = item['href']

        if ann_url not in links:
            print(ann_url)
            links.append(ann_url)
            titles.append(re.sub('\s+', ' ', item.contents[0].strip()))

            description_item = elem.find(class_='description', text=True)
            descriptions.append(re.sub('\s+', ' ', description_item.contents[0]))

            tmp_page = r.get(ann_url)
            this_page_soup = BeautifulSoup(tmp_page.text, 'html.parser')

            # we go to the announcement page to get better informations about the workplace and the date the job
            # announcement was issued

            locale_item = this_page_soup.find(class_='vip__location')
            location = locale_item.find('span')
            locations.append(re.sub('\s+', ' ', location.text))

            for block_item in this_page_soup.find_all(class_='vip__informations__block'):
                for span_item in block_item.find_all('span', {'class': 'vip__informations__value'}):
                    if "/" in span_item.text:
                        timestamps.append(re.sub('\s+', ' ', span_item.text))


            # Use this piece of code instead of the previous one if you aren't bothered to collect precise informations
            # about work locations and timestamps of announcements.

            # location_item = elem.find(class_='locale', text=True)
            # locations.append(location_item.contents[0])
            # timestamp_item = elem.find(class_='timestamp', text=True)
            # timestamps.append(timestamp_item.contents[0])
        else:
            print('announcement ' + ann_url + ' is already present')

    sleep_time = randint(1, 3)
    time.sleep(sleep_time)
    print('sleeping for ' + str(sleep_time) + 's')
    count += 1

# save jobs in tsv file
with open('jobs.tsv', 'a') as tsv_file:
    for i in range(len(links) - 1):
        try:
            row = titles[i] + '\t' + descriptions[i] + '\t' + locations[i] + '\t' + timestamps[i] + '\t' + \
                  links[i] + '\n'
        except IndexError:
            continue
        tsv_file.write(str(row))
