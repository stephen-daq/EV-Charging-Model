# retrieves 15 min interval LMP data at a given node
# output in DataFrame form or output to csv file

from datetime import time, timedelta
from pycaiso.oasis import Node
from threading import Thread
import pandas as pd
import time
import sys


class Prices:

  def __init__(self, start, end, nd, slp=1, excpt=30):

    self.starttime = start.replace(tzinfo=None)
    self.endtime = end.replace(tzinfo=None)
    self.node = Node(nd)
    self.sleeptime = slp
    self.excepttime = excpt
    self.prices = []
    self.ld = True
    self.api_wait = False

    t1 = Thread(target=Prices.__init_prices, args=(self,))
    t2 = Thread(target=Prices.__loading, args=(self,))

    t1.start()
    t2.start()

    t1.join()


  def __init_prices(self):

    start = self.starttime
    end = self.endtime



    curr = start
    ret = []

    while True:

      curr_end = curr + timedelta(days=4)

      try:

        if curr_end >= end:
          ret.append(self.node.get_lmps(curr, end))
          break

        ret.append(self.node.get_lmps(curr, curr_end))

        curr = curr_end

      except Exception as e:

        self.api_wait = True
        time.sleep(self.excepttime)
        self.api_wait = False


      time.sleep(self.sleeptime)

    self.prices = pd.concat(ret)
    self.ld = False

  def __loading(self):

    i = 1
    while self.ld:

      a = 'Requesting URL' + '.' * i

      if self.api_wait:
        a = 'Waiting for more API requests' + '.' * i

      sys.stdout.write('\r'+a) # Cursor up one line
      time.sleep(1)

      i = (i % 3) + 1


  def get_prices(self):
    return self.prices

  def get_starttime(self):
    return self.starttime

  def get_endtime(self):
    return self.endtime

  def to_file(self, path):
    df = pd.DataFrame(self.prices)
    df.to_csv(path + '/price.csv')