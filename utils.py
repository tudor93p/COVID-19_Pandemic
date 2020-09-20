from RO_data.counties import Counties as RoCounties
from RO_data.Ro_datelazi import RoCases
#from CH_data.


POP_FACTOR = 100000
ASCII = True


def select_country_specific_objects(country):
    """Initialize the country specific objects.
    
    Parameters
    ----------
    country: str
    """
    if country in ['RO','Romania','România']:
    
        cases = RoCases(root="RO_data/")
   
        
        counties = RoCounties(
    			"RO",
                        root = "RO_data/",
    			country_nameASCII="Romania",
    			country_name="România",
    			PopFactor=POP_FACTOR)


    else:
        raise NotImplementedError(f"Country name/code '{country}' not recognized or not yet implemented.")
    
    return cases, counties




#===========================================================================#
#
# Certain countries have a well-defined criterion to decide when to apply
#       restrictions for travellers from another country
#       
#       Germany: 50 new cases @100k in the last 14 days
#       Switz. : 60 ---"---
#
#---------------------------------------------------------------------------#


def quarantine_limit_(country):

    if country in ["CH","Switzerland","Schweiz"]:
        return 100000/POP_FACTOR* 60/14

    if country in ["Germany","DE","Deutschland"]:
        return 100000/POP_FACTOR* 50/14


    raise NotImplementedError(f"The limit allowed by country with name/code '{country}' not known.")

def quarantine_limit(country,data,per_capita=True,pop=1):
    
    if "infected" in data.lower():

        try:

            return (1 if per_capita else pop)*quarantine_limit_(country)

        except NotImplementedError:

            pass

    return None


#===========================================================================#
#
# For testing purposes
#
#---------------------------------------------------------------------------#

if __name__ == '__main__':

    cases,counties = select_country_specific_objects("RO")


    for n in ["infected","deceased","cured"]:
        for t in ["New","total"]:
    
            number = " ".join([t,n])
    
            data = cases.get_number(number)
    
            print(f"{number} today: {data}")

        print()
    print(counties.get_geoCountryBox())






