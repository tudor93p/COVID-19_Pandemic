#!/usr/bin/env python

import matplotlib.pyplot as plt
import pandas as pd

from RO_data.Ro_datelazi import RoCases


def get_population_pyramid(filename):
	df = pd.read_csv(filename)
	return parse_population_pyramid(df)


def parse_population_pyramid(dataframe):
	data_as_dict = {"0-9":  0, "10-19":  0, "20-29":  0, "30-39":  0, "40-49":  0, "50-59":  0, "60-69":  0, "70-79":  0, ">80":  0}
	for index, row in dataframe.iterrows():
		if index in [0, 1]:
			data_as_dict["0-9"] += row['M'] + row['F']
		elif index in [2, 3]:
			data_as_dict["10-19"] += row['M'] + row['F']
		elif index in [4, 5]:
			data_as_dict["20-29"] += row['M'] + row['F']
		elif index in [6, 7]:
			data_as_dict["30-39"] += row['M'] + row['F']
		elif index in [8, 9]:
			data_as_dict["40-49"] += row['M'] + row['F']
		elif index in [10, 11]:
			data_as_dict["50-59"] += row['M'] + row['F']
		elif index in [12, 13]:
			data_as_dict["60-69"] += row['M'] + row['F']
		elif index in [14, 15]:
			data_as_dict["70-79"] += row['M'] + row['F']
		elif index in [20]:
			pass
		else:
			data_as_dict[">80"] += row['M'] + row['F']
	return data_as_dict


def main():
	population_pyramid = get_population_pyramid('RO_data/Romania-2019.csv')

	cases_ro = RoCases()
	age_histogram = cases_ro.get_age_histogram()

	plt.bar(age_histogram.keys(), age_histogram.values(), color='g')
	plt.xlabel('Age group')
	plt.ylabel('Total cases')
	plt.show()

	plt.bar(population_pyramid.keys(), population_pyramid.values())
	plt.xlabel('Age group')
	plt.ylabel('Number of people')
	plt.title('Population pyramid')
	plt.show()

	normalized_by_population_pyramid = [100 * age_histogram[age_group]/population_pyramid[age_group] for age_group in list(age_histogram.keys())[:-1]]
	plt.bar(population_pyramid.keys(), normalized_by_population_pyramid, color='g')
	plt.xlabel('Age group [years]')
	plt.ylabel('Total cases normalized by population pyramid [%]')
	plt.show()


if __name__ == '__main__':
	main()
