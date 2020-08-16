import numpy as np
import json



#===========================================================================#
#
# Class with convenient methods
#
#---------------------------------------------------------------------------#

class RoCases:

  def __init__(self, fname):

    with open(fname, "r", encoding="latin-1") as f:

      data = json.load(f)

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

  def get_Day(self, iDay=None):
 
    if iDay is None:
      return self.days[-1]

    return self.days[iDay%len(self.days)]



  def get_iDay_Day(self, iDay=None, Day=None):

    if iDay is not None:
      return iDay%len(self.days), self.get_Day(iDay)
 
    if Day is not None:
      return self.get_iDay(Day), Day

    return self.get_iDay(Day), self.get_Day(iDay)
 

  def Nr_Infected(self, iDay=None, Day=None, County=None):

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




  def Nr_NewInfected(self, iDay=None, Day=None, TimeFrame=1, **kwargs):

    iDay, Day = self.get_iDay_Day(iDay, Day)

    today = self.Nr_Infected(iDay, Day=None, **kwargs)

    backthen = self.Nr_Infected(max(0, iDay-TimeFrame), Day=None, **kwargs)

    return today-backthen


  def Nr_Infected_AllDays(self, **kwargs):

    X = self.get_IndsDays()

    Y = [self.Nr_Infected(i, **kwargs, Day=None) for i in X]

    return np.array(X), np.array(Y)







  def Nr_NewInfected_AllDays(self, TimeFrame=1, **kwargs):

    X, Y = self.Nr_Infected_AllDays(**kwargs)

    return X, Y - np.append(np.zeros(TimeFrame), Y[:-TimeFrame])



#===========================================================================#
#
# test
#
#---------------------------------------------------------------------------#

if __name__ == '__main__':

  test = RoCases("Ro_data/date_15_august_la_13_00.json")

  print("Total today:", test.Nr_Infected())
  print("New today:", test.Nr_NewInfected())

  print("Total on", test.get_Day(43), ":", test.Nr_Infected(43))
  print("New on", test.get_Day(43), ":", test.Nr_NewInfected(43))

  print("Total on", test.get_Day(61), "in SB:", test.Nr_Infected(61, County="SB"))
  print("New on", test.get_Day(61), "in SB:", test.Nr_NewInfected(61, County="SB"))
