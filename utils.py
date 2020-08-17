from counties import Counties
from RO_data.Ro_datelazi import RoCases

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
    

        counties = Counties(
			"RO",
			country_nameASCII="Romania",
			country_name="România",
			PopFactor = POP_FACTOR)

    else:
        raise NotImplementedError("Country name/code '"+country+"' not recognized or not yet implemented.")

    return cases, counties
