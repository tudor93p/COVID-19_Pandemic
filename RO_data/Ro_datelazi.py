import numpy as np
import json
from datetime import datetime
import urllib.request

latest_fname = "latestData.json"


def load_data(fname, root=""):

	file_name = root + fname

	try:
		with open(file_name, encoding="latin-1") as f:
			data = json.load(f)
	except FileNotFoundError:
		file_name = 'RO_data/' + root + fname
		with open(file_name, encoding="latin-1") as f:
			data = json.load(f)

	local_date = data["charts"]["dailyStats"]["lastUpdatedOn"]

	new_date = datetime.now().strftime("%y-%m-%d")

	if local_date != new_date and datetime.now().hour > 12:

		url = 'https://di5ds1eotmbx1.cloudfront.net/latestData.json'

		open_url = urllib.request.urlopen(url)

		if open_url.getcode() == 200:
			data = json.loads(open_url.read())

		else:
			print("Error receiving data", open_url.getcode())

		with open(root+latest_fname, "w") as f:
			json.dump(data, f)

			print(f"Local data from {local_date} was updated to {data['charts']['dailyStats']['lastUpdatedOn']}")

	return data


class RoCases:
	"""Class with convenient methods."""

	def __init__(self, fname=latest_fname, root=""):

		data = load_data(fname, root)

		today = data["charts"]["dailyStats"]["lastUpdatedOn"]

		self.data = {**data["historicalData"], **{today: data["currentDayStats"]}}

		self.days = sorted(list(self.data.keys()))

		self.inds_days = {day: i for (i, day) in enumerate(self.days)}

	#    {i:day for (i, day) in enumerate(days)}

		self.counties = self.data[today]["countyInfectionsNumbers"].keys()

	def get_days(self):
		return self.days

	def get_IndsDays(self):
		return list(range(len(self.days)))

	def get_index_day(self, day=None):

		if day is None:
			return -1%len(self.days)

		return self.inds_days[day]

	def get_day(self, index_day=None):

		if index_day is None:
			return self.days[-1]

		return self.days[index_day % len(self.days)]

	def get_index_day_for_day(self, index_day=None, day=None):

		if index_day is not None:
			return index_day % len(self.days), self.get_day(index_day)

		if day is not None:
			return self.get_index_day(day), day

		return self.get_index_day(day), self.get_day(index_day)


	def get_number_infected_total(self, index_day=None, day=None, county=None):

		index_day, day = self.get_index_day_for_day(index_day, day)


		if county is None:
			return self.data[day]["numberInfected"]

		if county == "RO":
			return self.data[day]["numberInfected"]

		if county not in self.counties:
			return 0

		if "countyInfectionsNumbers" not in self.data[day].keys():
			return 0

		return self.data[day]["countyInfectionsNumbers"][county]

	def get_key_from_national_data_total(self, key, index_day=None, day=None, county=None):
		index_day, day = self.get_index_day_for_day(index_day, day)

		if county is None:
			return self.data[day][key]

		if county == "RO":
			return self.data[day][key]

		if county not in self.counties:
			return 0

	def get_key_from_national_data_new(self, key, index_day=None, day=None, time_frame=1, **kwargs):

		index_day, day = self.get_index_day_for_day(index_day, day)

		today = self.get_key_from_national_data_total(key, index_day, day=None, **kwargs)
		backthen = self.get_key_from_national_data_total(key, max(0, index_day - time_frame), day=None, **kwargs)

		return today-backthen

	def get_deceased_total(self, index_day=None, day=None, county=None):
		return self.get_key_from_national_data_total('numberDeceased', index_day, day, county)

	def get_deceased_new(self, index_day=None, day=None, time_frame=1, **kwargs):
		return self.get_key_from_national_data_new('numberDeceased', index_day, day, time_frame, **kwargs)

	def get_cured_total(self, index_day=None, day=None, county=None):
		return self.get_key_from_national_data_total('numberCured', index_day, day, county)

	def get_cured_new(self, index_day=None, day=None, time_frame=1, **kwargs):
		return self.get_key_from_national_data_new('numberCured', index_day, day, time_frame, **kwargs)

	def get_number_new_infected(self, index_day=None, day=None, time_frame=1, **kwargs):

		index_day, day = self.get_index_day_for_day(index_day, day)

		today = self.get_number_infected_total(index_day, day=None, **kwargs)

		backthen = self.get_number_infected_total(max(0, index_day - time_frame), day=None, **kwargs)

		return today-backthen


	def get_number_infected_all_days(self, **kwargs):

		x = self.get_IndsDays()

		y = [self.get_number_infected_total(i, **kwargs, day=None) for i in x]

		return np.array(x), np.array(y)

	def get_number_new_infected_all_days(self, time_frame=1, **kwargs):

		x, y = self.get_number_infected_all_days(**kwargs)

		return x, y - np.append(np.zeros(time_frame), y[:-time_frame])

	def get_age_histogram(self, index_day=None, day=None, county=None):
		return self.get_key_from_national_data_total('distributionByAge', index_day, day, county)

	def get_gender_stats(self, index_day=None, day=None, county=None):
		return self.get_key_from_national_data_total('genderStats', index_day, day, county)


if __name__ == '__main__':

	test = RoCases()

	print(f"Today: {test.get_day()}\n")

	print(f"Total cases today: {test.get_number_infected_total()}")
	print(f"New cases today: {test.get_number_new_infected()}\n")

	print(f"Deceased total: {test.get_deceased_total()}")
	print(f"Deceased today: {test.get_deceased_new()}\n")

	print(f"Cured total: {test.get_cured_total()}")
	print(f"Cured today: {test.get_cured_new()}\n")

	print(f"Age histogram: {test.get_age_histogram()}\n")

	# print(f"Total on {test.get_day(43)}: {test.get_number_infected(43)}")
	# print(f"New on {test.get_day(43)}: {test.get_number_new_infected(43)}\n")
	#
	# print(f"Total on {test.get_day(61)} in SB: {test.get_number_infected(61, county='SB')}")
	# print(f"New on {test.get_day(61)} in SB: {test.get_number_new_infected(61, county='SB')}\n")
