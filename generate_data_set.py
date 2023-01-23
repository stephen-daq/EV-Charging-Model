import csv
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

CALTECH_CHARGERS = 141
CALTECH_EMPLOYEES = 3500
CALTECH_STUDENTS = 2401
NORTHROP_EMPLOYEES = 18000

CHARGERS_PER_PERSON = CALTECH_CHARGERS / (CALTECH_STUDENTS + CALTECH_EMPLOYEES)
NORTHROP_CHARGERS = int(CHARGERS_PER_PERSON * NORTHROP_EMPLOYEES)
CHARGERS_RATIO = NORTHROP_CHARGERS/CALTECH_CHARGERS


def file_to_list(name):
	with open(f'{name}.csv', newline='') as file:
		reader = csv.reader(file)
		ret = np.array(list(reader))
	return ret


def list_to_file(lst, name):
	df = pd.DataFrame(lst)
	df.to_csv(f'{name}.csv')


def make_distribution(center, generations, peak=1, deviations=1):
    hour_indexes = 24

    normal_distribution = np.random.normal(loc=center, size=generations, scale=deviations)
    normal_distribution = [round(index) for index in normal_distribution]

    hours = np.zeros(hour_indexes)
    for index in normal_distribution:
        hours[index % hour_indexes] += 1

    hours = [hour / generations for hour in hours]
    scale = peak / max(hours)

    hours = [data_point * scale for data_point in hours]

    return hours


def get_error(estimation, target):
    error = [(estimation[index]-target[index])**2 for index in range(len(target)-1)]
    mse = sum(error) / len(error)
    return mse


def generate_pricing_day(ratio=1):
    price_estimate1 = make_distribution(18, 1000, peak=1.37, deviations=2.119)
    price_estimate2 = make_distribution(23, 1000, peak=0.31, deviations=2.04)

    price_estimate = list(np.array(price_estimate1) + np.array(price_estimate2))

    multiplied_estimate = [ratio * a for a in price_estimate]

    return multiplied_estimate