import sqlite3
import json
import time
from statistics import mean, StatisticsError

SQLITE_PATH = "db.sqlite"  # should make a config file
LIST_OF_GYMS_FILE = "gyms.txt"

class Database:

    def __init__(self):
        self.connection = sqlite3.connect(SQLITE_PATH)
        self.cursor = self.connection.cursor()
        self.gyms = open(LIST_OF_GYMS_FILE, 'r').read().strip().split('\n')

    def close(self):
        """
        Close the database and perform cleanup
        """

        self.connection.close()

    def create_database(self):

        for gym in self.gyms:
            operation = '''CREATE TABLE "{}" (Date TEXT, Day TEXT, Time TEXT, Num_people INTEGER)'''.format(gym)

            self.cursor.execute(operation)

            self.commit()

    def log_data(self, gym, date, day, time, num_people):

        operation = '''INSERT INTO `{}` VALUES (?, ?, ?, ?)'''.format(gym)
        self.cursor.execute(operation, (date, day, time, num_people))

    def commit(self):

        while True:
            try:
                self.connection.commit()
                break
            except sqlite3.OperationalError:
                print("Database locked, trying again")

    def get_raw_data_as_dictlist(self, gym):
        '''
        Return all observations for a given gym as a list. Each list item is a
        single observation containing the keys: date, day, time, num_people.
        '''

        # handle empty data?

        if gym not in self.gyms:
            return None

        operation = '''SELECT * FROM `{}` '''.format(gym)

        data = self.cursor.execute(operation).fetchall()
        data_formatted = []

        for observation in data:
            d = {}
            for index, field_label in enumerate(('date', 'day', 'time', 'num_people')):
                d[field_label] = observation[index]
            data_formatted.append(d)

        return data_formatted

    def get_raw_data_as_json(self, gym):
        return json.dumps(self.get_raw_data_as_dictlist(gym))

    def get_hour_summary_data_as_json(self, gym):

        raw_data = self.get_raw_data_as_dictlist(gym)

        days = [d for d in range(1, 8)]
        summary_data = {day: {hour: [] for hour in range(0, 24)} for day in days}

        for observation in raw_data:
            day = time.strptime(observation['day'], '%A').tm_wday + 1  # convert day to number (1-7)
            hour = int(observation['time'].split(':')[0])  # strip the hour value from the string
            summary_data[day][hour].append(observation['num_people'])

        for day in summary_data:
            for hour in summary_data[day]:
                try:
                    summary_data[day][hour] = mean(summary_data[day][hour])
                except StatisticsError:  # if no data points
                    summary_data[day][hour] = None

        return json.dumps(summary_data)







