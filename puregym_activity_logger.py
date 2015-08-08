#!/usr/bin/python3

import csv
from datetime import datetime
from time import sleep
from bs4 import BeautifulSoup
import urllib
import gzip

GYM_NAME = ""
GYM_URL = "http://puregym.com/gyms/%s/whats-happening" % GYM_NAME
CHECK_INTERVAL_MINUTES = 10
OUTPUT_FILE = "data.csv"


def get_page(url):

    try:
        html = urllib.request.urlopen(url)
    except urllib.error.HTTPError as e:
        print("HTTPError: " + str(e.code))
    except urllib.error.URLError as e:
        print("URLError: " + str(e.reason))
    else:
        if html.info().get('Content-Encoding') == 'gzip':
            return gzip.decompress(html.read())

        return html.read()

    return None


def extract_number_of_people(html):

    soup = BeautifulSoup(html, 'html.parser')
    return int(soup.find('span', {'class': 'people-number'}).contents[0])


def write_data(num_people, output_file):

    f = open(output_file, 'a')
    w = csv.writer(f)
    d = datetime.today()

    w.writerow([d.date(), d.strftime("%A"), d.strftime("%H:%M"), num_people])


while True:

    html = get_page(GYM_URL)

    if html:
        n = extract_number_of_people(html)
        write_data(n, OUTPUT_FILE)

        sleep(CHECK_INTERVAL_MINUTES * 60)

    html = None
