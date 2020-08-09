import numpy as np
import geopandas
import matplotlib.pyplot as plt

country = geopandas.read_file("gadm36_ROU.gpkg")


fig,(ax1,ax2) = plt.subplots(1,2)

country.plot(ax=ax1)

country[country['NAME_1']=="Suceava"].plot(ax=ax2)


plt.show()

