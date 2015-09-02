#!/usr/bin/python3

import csv
from datetime import datetime
from time import sleep
from bs4 import BeautifulSoup
import urllib.request
import gzip
import http
import sys

CHECK_INTERVAL_MINUTES = 10
OUTPUT_FILE = "data.csv"


def get_page(url):

    try:
        html = urllib.request.urlopen(url)
    except urllib.error.HTTPError as e:
        print("HTTPError: " + str(e.code))
    except urllib.error.URLError as e:
        print("URLError: " + str(e.reason))
    except http.client.HTTPException as e:
        print("HTTPException " + str(e.reason))
    else:
        if html.info().get('Content-Encoding') == 'gzip':
            return gzip.decompress(html.read())

        return html.read()

    return None


def extract_number_of_people(html):

    soup = BeautifulSoup(html, 'html.parser')
    try:
        num = int(soup.find('span', {'class': 'people-number'}).contents[0])
    except AttributeError:
        print("Couldn't find people-number class in the page.")
        return None
    else:
        return num


def write_data(num_people, output_file):

    f = open(output_file, 'a')
    w = csv.writer(f)
    d = datetime.today()

    w.writerow([d.date(), d.strftime("%A"), d.strftime("%H:%M"), num_people])

def watch_gym(gym_url):

    while True:

        html = get_page(gym_url)

        if html:
            n = extract_number_of_people(html)
            if n:
                write_data(n, OUTPUT_FILE)
            else:
                continue

            sleep(CHECK_INTERVAL_MINUTES * 60)

        html = None

if __name__ == "__main__":

    try:
        gym_name = sys.argv[1]
    except IndexError:
        gym_name = input("Enter the name of your gym: ")

    if gym_name:
        gym_url = "http://puregym.com/gyms/{}/whats-happening".format(gym_name)
        watch_gym(gym_url)
    else:
        raise ValueError("No gym name provided. Quitting.")
