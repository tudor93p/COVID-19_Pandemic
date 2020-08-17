import numpy as np
import geopandas
import matplotlib.pyplot as plt

country = geopandas.read_file("geodata.gpkg")


fig,axes = plt.subplots(2,2)

ax1,ax2,ax3,ax4 = axes.reshape(-1)

country.plot(ax=ax1)

country[country['NAME_1']=="Suceava"].plot(ax=ax2)

country[country['NAME_2']=="Medgidia"].plot(ax=ax3)

country[country['NAME_2']=="Falticeni"].plot(ax=ax4)

plt.show()

