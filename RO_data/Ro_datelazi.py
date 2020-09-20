import numpy as np
import json
from datetime import datetime
import urllib.request
from scipy.signal import savgol_filter

latest_fname = "latestData.json"



#===========================================================================#
#
# Load data from file or, if outdated or missing, from url
#
#---------------------------------------------------------------------------#


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
    
    new_date = datetime.now().strftime("%Y-%m-%d")
    
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



#===========================================================================#
#
# the class extracts the data
#
#---------------------------------------------------------------------------#


class RoCases:

    def __init__(self, fname=latest_fname, root=""):
    
        data = load_data(fname, root)
        
        today = data["charts"]["dailyStats"]["lastUpdatedOn"]
        
        self.data = {**data["historicalData"], **{today: data["currentDayStats"]}}
        
        self.days = sorted(list(self.data.keys()))
        
        self.inds_days = {day: i for (i, day) in enumerate(self.days)}
        
        
        self.counties = sorted(list(filter(lambda x: x!='-',
            self.data[today]["countyInfectionsNumbers"].keys())))


#===========================================================================#
#
# Methods to translate a day index to a day string and back
#
#---------------------------------------------------------------------------#


    def get_all_days(self):
        return self.days
    
    def get_indices_all_days(self):
    
        return np.arange(len(self.days))
    
    def get_dayindex(self, day=None):
    
        if day is None:
            return -1%len(self.days)
    
        return self.inds_days[day]
    
    def get_day(self, index_day=None):
    
        if index_day is None:
            return self.days[-1]
    
        return self.days[index_day % len(self.days)]
    
    def get_dayindex_and_day(self, index_day=None, day=None):
    
        new_day = self.get_day(index_day)
    
        new_index = self.get_dayindex(day)
    
        if index_day is not None:
    
            return index_day % len(self.days), new_day
        
        if day is not None:
    
            return new_index, day
        
        return new_index, new_day



#===========================================================================#
#
# extract certain data sets from the whole data dict 
#
#---------------------------------------------------------------------------#

    def get_key_from_national_data_total(self, key, countykey=None,
            index_day=None, day=None, county=None, time_frame=1, **kwargs):
    
        day = self.get_dayindex_and_day(index_day, day)[1]
        
        if county is None or county == "RO":
            return self.data[day][key]
        
        if county not in self.counties:
            return 0
        
        if countykey is None or countykey not in self.data[day].keys():
            return 0
        
        return self.data[day][countykey][county]
    
    
    
    def get_key_from_national_data_new(self, key, countykey=None,
            index_day=None, day=None, county=None, time_frame=1, **kwargs):
    
        index_today = self.get_dayindex_and_day(index_day, day)[0]
    
        return np.subtract(*[self.get_key_from_national_data_total(key, countykey, index_day, None, county) for index_day in [index_today,max(0, index_today - time_frame)]])
    
    

#===========================================================================#
#
# get (infected, deceased, cured)x(new, total) from the data dict
#
#---------------------------------------------------------------------------#

    def get_number(self, number, **kwargs):
   
        number = number.lower()

        for (n,k,ck) in [
            ('deceased','numberDeceased',None),
            ('cured','numberCured',None),
            ('infected','numberInfected','countyInfectionsNumbers')]:
    
            if n in number:
    
                if "total" in number:
    
                    return self.get_key_from_national_data_total(k, ck, **kwargs)
    
                if "new" in number:
                    return self.get_key_from_national_data_new(k, ck, **kwargs)
    
        raise NameError(f"Data requested ({number}) does not exist.")
   

    
    def get_numbers_all_days(self, number, time_frame=1, **kwargs):
    
        number = number.lower()
        

        x = self.get_indices_all_days()
    
        y = np.array([self.get_number(number.replace("new","total"),  **kwargs, day=None, index_day=i) for i in x])
    
            
        if "total" in number:
    
            return x,y
    
        if "new" in number:
    
            y_past = np.append(np.zeros(time_frame), y[:-time_frame])
    
            return x, y - y_past
   
    def smoothlabel(self,window=None,polyord=None,**kwargs):

        return " (smooth)" if window>1 and polyord>0 else ""


    def get_numbers_all_days_smooth(self, number, window=5, polyord=1, **kwargs):
        x, y = self.get_numbers_all_days(number, **kwargs)

        lab = self.smoothlabel(window,polyord)

        if window>1 and polyord>0:

            return x, savgol_filter(y,window,polyord), lab
    
        return x, y, lab
        

    def get_number_smooth(self, number, index_day=None, day=None, window=5,
            polyord = 1, **kwargs):

        if not (window>1 and polyord>0):

            return self.get_number(number, index_day=index_day, day=day, **kwargs),self.smoothlabel(window,polyord)


        index_day = self.get_dayindex_and_day(index_day,day)[0]
        
        x,y,label = self.get_numbers_all_days_smooth(number,window=window,
                polyord = polyord, **kwargs)


        return y[index_day], label
    

        


    def get_numbers_all_counties(self, number, **kwargs):

        y = [self.get_number(number, **kwargs, county = c) for c in self.counties]

        return np.arange(len(y)),np.array(y)


    def get_numbers_all_counties_smooth(self, number, **kwargs):

        y = [self.get_number_smooth(number, **kwargs, county = c)[0] for c in self.counties]

        return np.arange(len(y)), np.array(y), self.smoothlabel(**kwargs)



    def get_numbers_all_days_all_counties_smooth(self,number,**kwargs):

        y = np.arange(len(self.counties))

        x = self.get_indices_all_days()

        z = np.zeros((len(x),len(y)))

        
        for (i,c) in enumerate(self.counties):

            z[:,i] = self.get_numbers_all_days_smooth(number, **kwargs, county=c)[1]

        return x,y,z,self.smoothlabel(**kwargs)



#===========================================================================#
#
# Other data
#
#---------------------------------------------------------------------------#


    def get_age_histogram(self, index_day=None, day=None, county=None):
    
        return self.get_key_from_national_data_total('distributionByAge', None, index_day, day, county)
    
    def get_gender_stats(self, index_day=None, day=None, county=None):
    
        return self.get_key_from_national_data_total('genderStats', None, index_day, day, county)
    

#===========================================================================#
#
# For testing purposes
#
#---------------------------------------------------------------------------#

if __name__ == '__main__':

    test = RoCases()
    
    print(f"Today: {test.get_day()}\n")
    
    for n in ["infected","deceased","cured"]:
        for t in ["New","total"]:
    
            number = " ".join([t,n])
    
            data = test.get_number(number)
    
            print(f"{number} today: {data}")

        print()
    
    print(f"Age histogram today: {test.get_age_histogram()}\n")




