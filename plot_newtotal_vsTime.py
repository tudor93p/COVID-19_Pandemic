import matplotlib.pyplot as plt
import numpy as np


from utils import POP_FACTOR,ASCII,quarantine_limit

from plot_utils import extend_limits,minmax,collect_legends
from plot_utils import make_title,timestamp_to_date



#===========================================================================#
#
# Plotting function
#
#---------------------------------------------------------------------------#



def plot(ax1, Cases, Geo, data, day=None, county=None, prevdays=7,
        per_capita=False, window=5, polyord=1, show_mean=True, 
        show_total=True, title=None,
        show_countrylim=None, show_new=True, linewidth=4, **kwargs):



    if county is None:
        county = Geo.get_CountryName(ASCII=ASCII)
    
    
    
    
    ax1_2 = ax1.twinx()
    ax1_1 = ax1
    
    
    
    for ax in [ax1_1, ax1_2]:
        ax.ticklabel_format(axis='y', style='sci', scilimits=(-2,
            np.log10(999)))
    
   
    title = make_title(
                "Nr. data in county popfactor" if title is None else title,
                popfactor=(f"@ {POP_FACTOR} pop.")*per_capita,
                data=data,
                county=county,
                day=None if day is None else timestamp_to_date(day,month="long"),
                )

    if title is not None:
        ax1.set_title(title)


    
    countycode = Geo.get_Code(name=county)
    
    
    popfactor = 1/Geo.get_Pop(code=countycode) if per_capita else 1
    

       # ------------------------- #
   
    ax1_1.set_ylabel("Total")
   

    x11, y11 = Cases.get_numbers_all_days(f"total{data}",county=countycode)
    
    y11 = y11*popfactor
    
    if show_total:
        ax1_1.plot(x11, y11, label=f"Total {data}", c='darkorange', lw=linewidth*1.1)
    
    
    
    
    # -------------------------- #
    
    ax1_2.set_ylabel("New")
    
    x12, y12 = Cases.get_numbers_all_days(f"new{data}",county=countycode)
    
    y12 *= popfactor
    
    if show_new:
        ax1_2.vlines(x12, np.zeros_like(y12), y12, linewidth=linewidth/2,
              label=f"Daily new {data}", zorder=1, alpha=0.6)
    
    
    if show_mean:
        x14, y14, label14 = Cases.get_numbers_all_days_smooth(f"new{data}",window=window,polyord=polyord,time_frame=prevdays, county=countycode)

        y14 = y14 * popfactor/prevdays
   
        if prevdays == 1:

            label14 = "Daily new" +label14

        elif prevdays > 1:

            label14 = f"Mean last {prevdays} days" + label14

    
        ax1_2.plot(x14, y14, label=label14, c='navy', alpha=0.85, lw=linewidth, zorder=5)

        if data!="deceased":
        
            x15, y15, label15 = Cases.get_numbers_all_days_smooth(f"newdeceased",window=window,polyord=polyord,time_frame=prevdays, county=countycode)

   
            if np.sum(np.abs(y15))>0:

                y15 = y15 * popfactor/prevdays 

#                factor= int(min(y14/(y15+1e-20)))
                factor=10

                ax1_2.plot(x15, y15*factor, 
                        label=f"Deceased $\\times$ {factor}",
                        c='darkred', alpha=0.7, lw=linewidth*3/4, zorder=4)
     

    lim = quarantine_limit(show_countrylim,data,per_capita,Geo.get_Pop(code=countycode))
   
    if lim is not None:

        ax1_2.plot(ax1_2.get_xlim(), np.repeat(lim, 2), c="r", zorder=0,
                lw=linewidth/2, label=f"Criterion {show_countrylim}")

    # ------------------- #
    
    
    ax1.plot(ax1.get_xlim(), [0, 0], c="gray", zorder=0, lw=linewidth/3)
    
    
    
    ym12, yM12 = extend_limits(minmax(y12[np.arange(len(y12))!=16]), 0.07)
          # y12 can be negative
    ym12 = min(ym12, 0)
    
    if day is not None:
        ax1_2.plot(np.repeat(Cases.get_dayindex(day), 2), [ym12, yM12], c="crimson", zorder=0, lw=1.5 * linewidth, alpha=0.4)
    
    
    
    
    
    yM11 = extend_limits(minmax(y11), 0.07)[1]
          # y11 is only positive
    
    ym11 = yM11*ym12/(yM12 + 1e-20)
    
    ax1_2.set_ylim(ym12, yM12)
    ax1_1.set_ylim(ym11, yM11)
    
    
    
    ax1.set_xlim(0, np.max(np.append(x11, x12))+2)
    

    ax1.set_xticklabels([timestamp_to_date(Cases.get_day(int(x))) for x in ax1.get_xticks()])



    ax1_2.legend(*collect_legends(ax1_1, ax1_2), loc=9)
    
    

#===========================================================================#
#
# Adds to the pyqt figure specific sliders
#
#---------------------------------------------------------------------------#


    
def add_sliders(fig,cases,counties):

    fig.add_combobox(counties.CountyNames(include_country=True,ASCII=ASCII),
            label="County", key="county")

    fig.add_combobox(["infected","cured","deceased"], label="Data",
            key="data")

    fig.add_checkbox(label="Per capita", key="per" )

    fig.add_checkbox(label="Show new", key="new",status=True)
    
    fig.add_combobox(["None","Switzerland","Germany"],label="Country limit", key="countrylim" )
    
    fig.add_checkbox(label="Show mean", key="mean", status=True)
    
    fig.add_slider(label="Averaged days", key="prev", vs=np.arange(1, 30), v0=13, columnSpan=4)
    
    fig.add_slider(label="Smoothen", key="sg_w", vs=np.arange(1, 50, 2),  columnSpan=5 )
    
    fig.add_slider(label="Linewidth", key="lw", vs=np.linspace(0.5, 10, 20), v0=7, columnSpan=4)


def read_sliders(obj):

    return {    "data" : obj.get_combobox("data"),
           
                "county" : obj.get_combobox("county"),

                "prevdays" : obj.get_slider("prev"),

                "per_capita": obj.get_checkbox("per"),
                
                "window" : obj.get_slider("sg_w"),

                "show_mean" : obj.get_checkbox("mean"),

                "show_countrylim": obj.get_combobox("countrylim"),
                
                "show_new" : obj.get_checkbox("new"),
                
                "linewidth" : obj.get_slider("lw"),

            }





#===========================================================================#
#
# produces one figure
#
#---------------------------------------------------------------------------#



def main(country):

    from utils import select_country_specific_objects

    cases, counties = select_country_specific_objects(country)

   
    for data in ["infected","cured","deceased"]:
    
        fig, axes = plt.subplots(1, 1, figsize=(6, 4.5))
        
        plot(axes,
             cases,
             counties,
             data,
#             county="Suceava",
             per_capita = True,
             show_mean = True,
             show_new = True,
             show_countrylim="DE",
#             title="",
             )
        
        
        fig.tight_layout()
        
        break
    
    plt.show()
    
    plt.close()
    


if __name__ == '__main__':

  desired_country = 'Romania'
  main(desired_country)

