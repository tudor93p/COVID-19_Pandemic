import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import savgol_filter


from utils import select_country_specific_objects,POP_FACTOR,ASCII



def extend_limits(lim, amount=0.04):

  return np.array(lim) + np.diff(lim)*np.array([-1, 1])*amount

def minmax(A):

  return np.array([np.min(A), np.max(A)])


def plot(axes, Cases, Geo, county=None, day=None, showcases="Total", prevdays=7, per_capita=False, window=5, polyord=1, show_mean=True, show_CHlim=False, show_new=True,  linewidth=4, county_labels=True, county_capitals=False, cmap="viridis", vminmax=None, maxcolor=None):

    
  if day is None:
    day = Cases.get_Day()	# the last day
  if county is None:
    county = Geo.get_CountryName(ASCII=ASCII)



  ax1, ax2 = axes

  ax1.set_xlabel("Day index")

  ax1_2 = ax1.twinx()
  ax1_1 = ax1



  for ax in [ax1_1, ax1_2]:
    ax.ticklabel_format(axis='y', style='sci', scilimits=(-2, 2))


  ax1.set_title("Stats for "+county + (" (@ "+str(POP_FACTOR)+" pop.)")*per_capita)


  countycode = Geo.get_Code(name=county)


  popfactor = 1/Geo.get_Pop(code=countycode) if per_capita else 1

 # ------------------------- #

  ax1_1.set_ylabel("Total cases")

  x11, y11 = Cases.Nr_Infected_AllDays(County=countycode)

  y11 = y11*popfactor


  ax1_1.plot(x11, y11, label="Total", c='darkorange', lw=linewidth*1.1)




  # -------------------------- #

  ax1_2.set_ylabel("New cases")

  x12, y12 = Cases.Nr_NewInfected_AllDays(County=countycode)

  y12 *= popfactor

  if show_new:
    ax1_2.vlines(x12, np.zeros_like(y12), y12, linewidth=linewidth/2, label="Daily new", zorder=1, alpha=0.6)

  x14, y14 = Cases.Nr_NewInfected_AllDays(TimeFrame=prevdays, County=countycode)

  y14 *= popfactor/prevdays

  label14="Daily new" if prevdays==1 else "Mean last "+str(prevdays)+" days"

  if window!=1 and polyord!=0:

    y14 = savgol_filter(y14, window, polyord)

    label14 = label14 + " (smooth)"

  if show_mean:
    ax1_2.plot(x14, y14, label=label14, c='navy', alpha=0.85, lw=linewidth, zorder=5)


  if show_CHlim:
    CH_lim = Geo.get_Pop(code=countycode)*POP_FACTOR/100000*(60/14)*popfactor

    ax1_2.plot(ax1_2.get_xlim(), np.repeat(CH_lim, 2), c="r", zorder=0, lw=linewidth/2, label="Criterion CH")



  # ------------------- #


  ax1.plot(ax1.get_xlim(), [0, 0], c="gray", zorder=0, lw=linewidth/3)



  ym12, yM12 = extend_limits(minmax(y12[np.arange(len(y12))!=16]), 0.07)
	# y12 can be negative
  ym12 = min(ym12, 0)

  ax1_2.plot(np.repeat(Cases.get_iDay(day), 2), [ym12, yM12], c="crimson", zorder=0, lw=1.5*linewidth, alpha=0.4)





  yM11 = extend_limits(minmax(y11), 0.07)[1]
	# y11 is only positive

  ym11 = yM11*ym12/yM12

  ax1_2.set_ylim(ym12, yM12)
  ax1_1.set_ylim(ym11, yM11)



  for (i, ax) in enumerate([ax1_1, ax1_2]):

    ax.set_xlim(0, np.max(np.append(x11, x12))+2)


  lines1,  labels1 = ax1_1.get_legend_handles_labels()

  lines2,  labels2 = ax1_2.get_legend_handles_labels()

  ax1_2.legend(lines1 + lines2,  labels1 + labels2,  loc=9)



  # ----------------- #


  for cc in Geo.get_CodeList(include_country=False):

    if showcases == "Total":

      tot = Cases.Nr_Infected(Day=day, County=cc)

      Geo.set_geoColumn(showcases, tot*popfactor, code=cc)

      label2 = "Total cases"

    elif showcases == "New":

      label2 = "Daily new" if prevdays==1 else "Mean last "+str(prevdays)+" days"
      if window!=1 and polyord!=0:

        y2 = Cases.Nr_NewInfected_AllDays(TimeFrame=prevdays, County=cc)[1]

        new = savgol_filter(y2, window, polyord)[Cases.get_iDay(day)]

        label2 = label2 + " (smooth)"

      else:
        new = Cases.Nr_NewInfected(Day=day, TimeFrame=prevdays, County=cc)

      Geo.set_geoColumn(showcases, new*popfactor/prevdays, code=cc)

    if county_labels:

      if cc != "B": # there's no space for 'B'

        if cc=="IF":
#          xy = Geo.get_geoCapCoord(code=cc)

          ha, va = 'left', 'bottom'


        else:
          ha, va = 'center', 'center'

        xy = Geo.get_geoCenter(code=cc)

        ax2.text(*xy, str(cc), verticalalignment=va, horizontalalignment=ha, zorder=4, color="k" if cmap in ["cool", "PuBuGn", "YlGnBu", "Spectral", "coolwarm"] else "w")
#      ax2.scatter(*Geo.get_geoCapCoord(code=cc), c='r', s=2, zorder=2)


  if county_capitals:
    ax2.scatter(*Geo.get_geoCapCoord_All().T, c='r', s=2, zorder=2)

  ax2.set_xticks([])
  ax2.set_yticks([])
  ax2.set_xlabel("")
  ax2.set_ylabel("")


  xlim, ylim = Geo.get_geoCountryBox()

  ax2.set_xlim(xlim)
  ax2.set_ylim(ylim)

  ax2.set_axis_off()

  if vminmax is None:
    vmin = 0
    vmax = np.max(Geo.get_geoColumn(showcases))

  else:
    vmin, vmax = vminmax

  if maxcolor is not None:
    vmax *= maxcolor

  Geo.plot(ax=ax2, column=showcases, cmap=cmap, zorder=0, legend=True, legend_kwds={'orientation':"horizontal", "pad":0.05, 'label':" ".join([day+":", label2]+[" (@ "+str(POP_FACTOR)+" pop.)"]*per_capita)}, vmin=vmin, vmax=vmax)

  return np.sort([np.max(Geo.get_geoColumn(showcases, code=cc)) for cc in Geo.get_CodeList(include_country=False) if cc not in ["B", "SV"]])








def main(country):

  cases, counties = select_country_specific_objects(country)

  for (cmap, showcases) in zip(["YlGnBu",  "viridis"], ["New", "Total"]):

    fig, axes = plt.subplots(1, 2, figsize=(10, 4.6))

    P = plot(	axes,
		cases,
		counties,
	      	per_capita = True,
	      	showcases = showcases,
	      	cmap = cmap,
	      	show_mean = True,
	      	show_new = True,
      		show_CHlim = True,
	      	)		

    print(P)

    fig.tight_layout()

    break

  plt.show()

  plt.close()





if __name__ == '__main__':

  desired_country = 'Romania'
  main(desired_country)

