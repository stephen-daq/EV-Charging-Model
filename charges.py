# retrieves charging session data
# output in DataFrame form or output to csv file

from datetime import datetime, time
from threading import Thread
import pandas as pd
import api_keys
import requests
import time
import pytz
import sys


class Charges:

  def __init__(self, start, end):
    self.start_datetime = start.astimezone(tz=pytz.utc).replace(tzinfo=None)
    self.end_datetime = end.astimezone(tz=pytz.utc).replace(tzinfo=None)
    self.load = True
    self.sessions = []

    initialize = Thread(target=Charges.__init_sessions, args=(self,))
    loading = Thread(target=Charges.__loading, args=(self,))

    initialize.start()
    loading.start()

    initialize.join()

  def __init_sessions(self):
    start = self.start_datetime
    end = self.end_datetime

    self.sessions = []

    end_filter = "connectionTime<=\""
    end_filter += end.strftime('%a, %d %b %Y %H:%M:%S %Z') + " GMT\""

    while True:

      token = api_keys.charges
      url = 'https://ev.caltech.edu/api/v1/sessions/caltech'

      start_filter = "where=connectionTime>=\""
      start_filter += start.strftime('%a, %d %b %Y %H:%M:%S %Z') + " GMT\""

      request_string =  url + '?' + start_filter + ' and ' + end_filter 

      try:
        request = requests.get(request_string, auth=(token, "")).json()['_items']

      except:
        break

      if len(request) == 1:
        self.end_datetime = start
        break

      for charge in request:
        self.sessions.append(charge)

      start_string = self.sessions[-1]['connectionTime']
      start = datetime.strptime(start_string, '%a, %d %b %Y %H:%M:%S %Z')

    self.load = False

  def __loading(self):

    i = 1
    while self.load:

      load_message = 'Requesting URL' + '.' * i
      sys.stdout.write('\r'+ load_message)
      time.sleep(1)

      i = (i % 3) + 1


  def get_sessions(self):
    return self.sessions

  def get_starttime(self):
    return self.start_datetime

  def get_endtime(self):
    return self.end_datetime

  def to_file(self, path):
    sessions_df = pd.DataFrame(self.sessions)
    sessions_df.to_csv(path + '\\charge.csv')