import csv
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn import metrics
from sklearn import kernel_ridge
from sklearn import linear_model
from sklearn import neural_network
from datetime import datetime, timedelta

svm_kernels = [
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

	with open(f'{name}.csv', newline='') as file:
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

def get_ridge_kernels(errs):
	ridge_kernels = metrics.pairwise.PAIRWISE_KERNEL_FUNCTIONS
	ridge_kernels = list(ridge_kernels.keys())
	ridge_kernels.remove('chi2')

	for m in ridge_kernels:
		ridge = kernel_ridge.KernelRidge(kernel=m)
		ridge.fit(hours[::2], prices[::2])

		ridge_prediction = ridge.predict(hours[1::2])
		score = ridge.score(hours[1::2], prices[1::2])

		plt.plot(prices[1::2], color='blue')
		plt.plot(ridge_prediction, color='orange')

		plt.savefig(f'results\\kernel_ridge_{m}.png')
		errs.append([f'kernel_ridge_{m}', score])
	
	return errs

def get_mlp(errs, tol=0.0001):
	activation = ['identity', 'logistic', 'tanh', 'relu']
	solver = ['lbfgs', 'sgd', 'adam']

	for a in activation:
		for s in solver:
			try:
				regressor = neural_network.MLPRegressor(activation=a, solver=s, max_iter=1000, tol=tol)
				regressor.fit(hours[::2], prices[::2])

				prediction = regressor.predict(hours[1::2])
				score = regressor.score(hours[1::2], prices[1::2])

				plt.plot(prices[1::2], color='blue')
				plt.plot(prediction, color='orange')

				plt.savefig(f'results\\mlp_act={a}_sol={s}.png')
				errs.append([f'mlp_act={a}_sol={s}', score])

			except:
				print(f'act={a} sol={s}')
				
	return errs


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

h = file_to_list('data\\hours')
p = file_to_list('data\\prices')

hours = []
prices = list(map(float, p[1:,1]))

for i in h[2:,1:]:
	for a in i:
		try:
			if float(a) < 0:
				i[4] = 0
		except:
			pass
		
	temp = [float(i[0]), int(bool(i[1])), float(i[2]), float(i[3]), float(i[4]), float(i[5]), float(i[6]), float(i[7])]
	hours.append(temp)

errors = list(file_to_list('results\\model_errors')[1:,1:])



list_to_file(errors, 'results\\model_errors')
				

#lin_regression = linear.LinearRegression()

'''

for model in svm_models:
	predict = svm.SVR(kernel=model, C=0.1)
	predict.fit(hours[::2], prices[::2])

	prediction = predict.predict(hours[1::2])
	plt.plot(prices[1::2], color='blue')
	plt.plot(prediction, color='orange')
	plt.savefig(f'{model}.png')
'''