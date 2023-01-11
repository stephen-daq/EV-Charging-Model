
import csv
import numpy as np
import pandas as pd
import sklearn.svm as svm
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

models = [
	'linear',
	'poly',
	'rbf',
	'sigmoid'
]

colors = [
	'orange',
	'yellow',
	'purple',
	'green'
]

def string_to_datetime1(datetime_string):
	return datetime.strptime(datetime_string, '%a, %d %b %Y %H:%M:%S %Z')


def string_to_datetime2(datetime_string):
	return datetime.strptime(datetime_string, '%Y-%m-%dT%H:%M')


def datetime_to_string(dt):
	return f'{dt.month}/{dt.day}/{dt.year} {dt.hour}:00'


def file_to_list(name):

	with open(name, newline='') as file:
		reader = csv.reader(file)
		ret = np.array(list(reader))
	return ret


def list_to_file(lst, name):
	df = pd.DataFrame(lst)
	df.to_csv(f'{name}.csv')


def get_kwh_in_intervals(charges, start, end):
	kwh_per_hour = []

	while start < end:
		kwh_per_hour.append([start, 0])

		for charge in charges:
			coef = 0
			interval = 0

			if charge[2] > start and charge[0] < (start + timedelta(hours=1)):
				start_interval = max([start, charge[0]])
				end_interval = min(start + timedelta(hours=1), charge[2])

				coef = ((end_interval - start_interval) / (charge[2] - charge[0]))

				kwh_per_hour[-1][1] += coef * charge[1]

		start = start + timedelta(hours=1)

	return kwh_per_hour


def charge_to_datetimes(charges):
	charges_dt = []

	for a in charges[1:]:
		try:
			start = string_to_datetime1(a[9])
			power = float(a[11])
			end = string_to_datetime1(a[12])
			charges_dt.append([start, power, end])
		except:
			pass
							
	return charges_dt


def weather_to_datetime(weather_unformatted):
	weather = [['time', 'temperature', 'precipitation', 'direct_radiation']]

	for w in weather_unformatted[1:]:
		weather.append([string_to_datetime2(w[0]), float(w[1]), float(w[2]), float(w[3])])

	return weather

'''
weather = file_to_list('weather.csv')
kwhs = file_to_list('kwh_interval.csv')
prices = file_to_list('price.csv')

hours = [['Month', 'Weekday', 'Second', 'Days from solstice', 'Temperature', 'Precipitation', 'Solar irradiance', 'KWH supplied']]

iterative_datetime = datetime(2018, 10, 1)
iteration = 0

while iterative_datetime < datetime(2019, 3, 18):
	month = iterative_datetime.month
	weekday = iterative_datetime.weekday()
	second = iterative_datetime.hour * 3600
	days_from_solstice = abs((iterative_datetime - datetime(2018, 12, 21)).days)

	hourly_info = [month, weekday, second, days_from_solstice]

	iterative_datetime_string = datetime_to_string(iterative_datetime)

	weather_info = (weather[2:])[iteration][2:]
	[hourly_info.append(float(w)) for w in weather_info]

	hourly_info.append(kwhs[iteration + 1][2])

	hours.append(hourly_info)

	iterative_datetime = iterative_datetime + timedelta(hours=1)
	iteration += 1

hours = np.array(hours)
list_to_file(hours, 'hours')
'''
h = file_to_list('hours.csv')
p = file_to_list('prices.csv')


hours = []
prices = list(map(float, p[1:,1]))

for i in h[2:,1:]:
	try:
		hours.append( list(map(float,i)) )
	except:
		pass


[a.pop(2) for a in hours]

plt.plot(prices[:3000], color='blue')

for i in range(4):
	predict = svm.SVR(kernel=models[i], C=5)
	predict.fit(hours[:3000], prices[:3000])

	plt.plot(predict.predict(hours[:3000]), color=colors[i])

plt.show()