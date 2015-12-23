#!/usr/bin/python3

from database import Database
from datetime import datetime
from time import sleep
from bs4 import BeautifulSoup
import urllib.request
import gzip
import http

CHECK_INTERVAL_MINUTES = 10
DATA_SUBDIRECTORY = "recorded_data"
LIST_OF_GYMS_FILE = "gyms.txt"


class PureGymLogger:

    def __init__(self):
        self.gyms = open(LIST_OF_GYMS_FILE, 'r').read().strip().split('\n')
        self.db = Database()

    def get_page(self, url):

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

    def extract_number_of_people(self, html):

        soup = BeautifulSoup(html, 'html.parser')
        try:
            num = int(soup.find('span', {'class': 'people-number'}).contents[0])
        except AttributeError:
            print("Couldn't find people-number class in the page.")
            return None
        else:
            return num

    def write_data(self, num_people, gym_name):

        d = datetime.utcnow()
        self.db.log_data(gym_name, d.date(), d.strftime("%A"), d.strftime("%H:%M"), num_people)

    def find_number_of_people_in_gym(self, gym_name):

        attempts = 0
        while attempts < 3:

            print("Watching gym {}, attempt {}".format(gym_name, attempts))
            html = self.get_page("http://puregym.com/gyms/{}/whats-happening".format(gym_name))

            if html:
                n = self.extract_number_of_people(html)
                if n:
                    print("{} people are in {}".format(n, gym_name))
                    self.write_data(n, gym_name)
                    break
                else:
                    print("broke")

                print('Wrote data at {}'.format(datetime.utcnow()))

            attempts += 1

    def watch_gyms(self):

        while True:
            for gym in self.gyms:

                # write number of people in gymto file here
                self.find_number_of_people_in_gym(gym)

            self.db.commit()
            print("Waiting")
            sleep(CHECK_INTERVAL_MINUTES * 60)


if __name__ == "__main__":

    p = PureGymLogger()
    p.watch_gyms()


