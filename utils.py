from counties import Counties
from Ro_datelazi import RoCases


def select_country_specific_objects(country):
    """Initialize the country specific objects.

    Parameters
    ----------
    country: str
    """
    if country == 'Romania':
        cases = RoCases("Ro_data/date_15_august_la_13_00.json")
        pop_factor = 100000
        country = "Ro_data/"
        counties = Counties(root=country, PopFactor=pop_factor)
    else:
        raise NotImplementedError('Country name not recognized or not yet implemented.')

    return cases, counties
