import numpy as np
import json
from datetime import datetime
import urllib.request

latest_fname = "latestData.json"


def load_data(fname,root=""):

	with open(root+fname, "r", encoding="latin-1") as f:

		data = json.load(f)


	local_date = data["charts"]["dailyStats"]["lastUpdatedOn"]

	new_date = datetime.now().strftime("%Y-%m-%d")


	if local_date != new_date and datetime.now().hour > 12:

		url = 'https://di5ds1eotmbx1.cloudfront.net/latestData.json'

		operUrl = urllib.request.urlopen(url)

		if(operUrl.getcode()==200):
			 data = json.loads(operUrl.read())

		else:
			 print("Error receiving data", operUrl.getcode())

		with open(root+latest_fname,"w") as f:
			json.dump(data,f)

			print("Local data from",local_date," was updated to",data["charts"]["dailyStats"]["lastUpdatedOn"])




	return data

#===========================================================================#
#
# Class with convenient methods
#
#---------------------------------------------------------------------------#

class RoCases:

	def __init__(self,fname = latest_fname, root=""):

		data = load_data(fname,root)

		today = data["charts"]["dailyStats"]["lastUpdatedOn"]

		self.data = {**data["historicalData"], **{today: data["currentDayStats"]}}

		self.days = sorted(list(self.data.keys()))

		self.inds_days = {day:i for (i, day) in enumerate(self.days)}

	#    {i:day for (i, day) in enumerate(days)}

		self.counties = self.data[today]["countyInfectionsNumbers"].keys()

	def get_Days(self):
		return self.days


	def get_IndsDays(self):
		return list(range(len(self.days)))


	def get_iDay(self, Day=None):

		if Day is None:
			return -1%len(self.days)

		return self.inds_days[Day]

	def get_day(self, iDay=None):

		if iDay is None:
			return self.days[-1]

		return self.days[iDay%len(self.days)]

	def get_iDay_Day(self, iDay=None, Day=None):

		if iDay is not None:
			return iDay%len(self.days), self.get_day(iDay)

		if Day is not None:
			return self.get_iDay(Day), Day

		return self.get_iDay(Day), self.get_day(iDay)


	def get_number_infected(self, iDay=None, Day=None, County=None):

		iDay, Day = self.get_iDay_Day(iDay, Day)


		if County is None:
			return self.data[Day]["numberInfected"]

		if County == "RO":
			return self.data[Day]["numberInfected"]

		if County not in self.counties:
			return 0

		if "countyInfectionsNumbers" not in self.data[Day].keys():
			return 0

		return self.data[Day]["countyInfectionsNumbers"][County]

	def get_key_from_national_data_total(self, key, iDay=None, Day=None, County=None):
		iDay, Day = self.get_iDay_Day(iDay, Day)

		if County is None:
			return self.data[Day][key]

		if County == "RO":
			return self.data[Day][key]

		if County not in self.counties:
			return 0

	def get_key_from_national_data_new(self, key, iDay=None, Day=None, TimeFrame=1, **kwargs):

		iDay, Day = self.get_iDay_Day(iDay, Day)

		today = self.get_key_from_national_data_total(key, iDay, Day=None, **kwargs)
		backthen = self.get_key_from_national_data_total(key, max(0, iDay - TimeFrame), Day=None, **kwargs)

		return today-backthen

	def get_deceased_total(self, iDay=None, Day=None, County=None):
		return self.get_key_from_national_data_total('numberDeceased', iDay, Day, County)

	def get_deceased_new(self, iDay=None, Day=None, TimeFrame=1, **kwargs):
		return self.get_key_from_national_data_new('numberDeceased', iDay, Day, TimeFrame, **kwargs)

	def get_cured_total(self, iDay=None, Day=None, County=None):
		return self.get_key_from_national_data_total('numberCured', iDay, Day, County)

	def get_cured_new(self, iDay=None, Day=None, TimeFrame=1, **kwargs):
		return self.get_key_from_national_data_new('numberCured', iDay, Day, TimeFrame, **kwargs)

	def get_number_new_infected(self, iDay=None, Day=None, TimeFrame=1, **kwargs):

		iDay, Day = self.get_iDay_Day(iDay, Day)

		today = self.get_number_infected(iDay, Day=None, **kwargs)

		backthen = self.get_number_infected(max(0, iDay - TimeFrame), Day=None, **kwargs)

		return today-backthen



	def get_number_infected_all_days(self, **kwargs):

		X = self.get_IndsDays()

		Y = [self.get_number_infected(i, **kwargs, Day=None) for i in X]

		return np.array(X), np.array(Y)

	def get_number_new_infected_all_days(self, TimeFrame=1, **kwargs):

		X, Y = self.get_number_infected_all_days(**kwargs)

		return X, Y - np.append(np.zeros(TimeFrame), Y[:-TimeFrame])



#===========================================================================#
#
# test
#
#---------------------------------------------------------------------------#


if __name__ == '__main__':

	test = RoCases()

	print(f"Today: {test.get_day()}\n")

	print(f"Total cases today: {test.get_number_infected()}")
	print(f"New cases today: {test.get_number_new_infected()}\n")

	print(f"Deceased total: {test.get_deceased_total()}")
	print(f"Deceased today: {test.get_deceased_new()}\n")

	print(f"Cured total: {test.get_cured_total()}")
	print(f"Cured today: {test.get_cured_new()}\n")

	print(f"Total on {test.get_day(43)}: {test.get_number_infected(43)}")
	print(f"New on {test.get_day(43)}: {test.get_number_new_infected(43)}\n")

	print(f"Total on {test.get_day(61)} in SB: {test.get_number_infected(61, County='SB')}")
	print(f"New on {test.get_day(61)} in SB: {test.get_number_new_infected(61, County='SB')}\n")
