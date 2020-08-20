import numpy as np
from datetime import datetime
import urllib.request
import pandas as pd


latest_fname = "latestData.csv"


def load_data(fname,root=""):
    
    data = pd.read_csv(root+fname,low_memory=False)

    today = datetime.now().date()

    date_localdata = pd.Timestamp(data['replikation_dt'][0]).date()

    if date_localdata<today and datetime.now().hour > 15:



#    url = "https://www.bag.admin.ch/dam/bag/de/dokumente/mt/k-und-i/aktuelle-ausbrueche-pandemien/2019-nCoV/covid-19-basisdaten-bevoelkerungszahlen.xlsx.download.xlsx/Population_Size_BFS.xlsx"
        
        url = "https://www.bag.admin.ch/dam/bag/de/dokumente/mt/k-und-i/aktuelle-ausbrueche-pandemien/2019-nCoV/covid-19-basisdaten-fallzahlen.xlsx.download.xlsx/Dashboards_1&2_COVID19_swiss_data_pv.xlsx"



        openUrl = urllib.request.urlopen(url)
  
        if(openUrl.getcode()==200):

            data = pd.read_excel(openUrl.read(), sheet_name=None)['Dashboard_1_2']

        else:
            print("Error receiving data", openUrl.getcode())



#    with open(root+latest_fname,"w") as f:
#        json.dump(data,f)

        data.to_csv(root+latest_fname)
    
        print("Local data from",date_localdata," was updated to", data['replikation_dt'][0].date())



        data = pd.read_csv(root+latest_fname,low_memory=False)

    return data

#===========================================================================#
#
# Class with convenient methods
#
#---------------------------------------------------------------------------#

class CH_Cases:

    def __init__(self,fname = latest_fname, root=""):

        self.data = load_data(fname,root)


#    today = data["charts"]["dailyStats"]["lastUpdatedOn"]
#
#    self.data = {**data["historicalData"], **{today: data["currentDayStats"]}}
#
#    self.days = sorted(list(self.data.keys()))
#
#    self.inds_days = {day:i for (i, day) in enumerate(self.days)}
#
##    {i:day for (i, day) in enumerate(days)}
#
#    self.counties = self.data[today]["countyInfectionsNumbers"].keys()


















#===========================================================================#
#
# test
#
#---------------------------------------------------------------------------#

if __name__ == '__main__':



    test = CH_Cases()
    print(test.data.keys())

            
    fall_dt = sorted(list(set(pd.to_datetime(test.data['fall_dt']).dt.date)))

    print("First case:",fall_dt[1])
    print("Last case:",fall_dt[-1])


    print("Some number related to",fall_dt[-1],
            sum(pd.to_datetime(test.data['fall_dt']).dt.date==fall_dt[-1]))
#To select rows whose column value equals a scalar, some_value, use ==:
#
#    df.loc[df['column_name'] == some_value]
#    To select rows whose column value is in an iterable, some_values, use
#    isin:
#
#        df.loc[df['column_name'].isin(some_values)]
#        Combine multiple conditions with &:
#
#            df.loc[(df['column_name'] >= A) & (df['column_name'] <= B)]i
#
#Note the parentheses. Due to Python's operator precedence rules, & binds more
#tightly than <= and >=. Thus, the parentheses in the last example are
#necessary. Without the parentheses
#
#df['column_name'] >= A & df['column_name'] <= B
#is parsed as
#
#df['column_name'] >= (A & df['column_name']) <= B
#which results in a Truth value of a Series is ambiguous error.
#
#To select rows whose column value does not equal some_value, use !=:
#
#    df.loc[df['column_name'] != some_value]
#    isin returns a boolean Series, so to select rows whose value is not in
#    some_values, negate the boolean Series using ~:
#
#        df.loc[~df['column_name'].isin(some_values)]


#print("Today:",test.get_Day())
#
#print("Total today:", test.Nr_Infected())
#print("New today:", test.Nr_NewInfected())
#
#print("Total on", test.get_Day(43), ":", test.Nr_Infected(43))
#print("New on", test.get_Day(43), ":", test.Nr_NewInfected(43))
#
#print("Total on", test.get_Day(61), "in SB:", test.Nr_Infected(61, County="SB"))
#print("New on", test.get_Day(61), "in SB:", test.Nr_NewInfected(61, County="SB"))
##
