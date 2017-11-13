import requests as r
from bs4 import BeautifulSoup
import os

page =  'https://www.kijiji.it/offerte-di-lavoro/'

jobs = ['informatica', 'grafica', 'web']

urls = []

if os.path.isfile('jobs.tsv'):
    os.remove('jobs.tsv')

for job in jobs:
    urls.append(r.get(page + job))

for url in urls:

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
        short_descriptions = []
        locations = []
        timestamps = []
        full_descriptions = []

        for elem in ann_list:

            for item in elem.find_all(class_='cta', href=True, text=True):
                links.append(item['href'])
                titles.append(item.contents[0].strip())

            for description_item in  elem.find_all(class_='description', text=True):
                short_descriptions.append(description_item.contents[0].replace('\n', ''))

            for location_item in elem.find_all(class_='locale', text=True):
                locations.append(location_item.contents[0])

            for timestamp_item in elem.find_all(class_='timestamp', text=True):
                timestamps.append(timestamp_item.contents[0])

        # print(titles)
        # print(short_descriptions)
        # print(locations)
        # print(timestamps)
        # print(links)

        with open('jobs.tsv', 'a') as tsv_file:
            for i in range(num_pages):
                try:
                    row = titles[i] + '\t' + short_descriptions[i] + '\t' + locations[i] + '\t' + timestamps[i] + '\t'\
                          + links[i] + '\n'
                except IndexError:
                    continue
                tsv_file.write(str(row))

        count += 1
