import matplotlib.pyplot as plt
import numpy as np


from utils import POP_FACTOR,ASCII,quarantine_limit

from plot_utils import extend_limits,minmax,collect_legends



#===========================================================================#
#
# Plotting function
#
#---------------------------------------------------------------------------#



def plot(ax1, Cases, Geo, data, day=None, prevdays=7, county=None,
        per_capita=False, window=5, polyord=1, show_mean=True,
        show_total = True, show_countrylim=None, linewidth=4, **kwargs):


    if day is None:
        day = Cases.get_day()	# the last day
   
    index_day = Cases.get_dayindex(day)
    
    
    ax1.set_xlabel("County index")
    
    ax1_2 = ax1.twinx()
    ax1_1 = ax1
    
    
    
    for ax in [ax1_1, ax1_2]:
        ax.ticklabel_format(axis='y', style='sci', scilimits=(-2, 2))

    ax1.set_title(f"Nr. {data} on {day}" 
                                + (f" (@ {POP_FACTOR} pop.)")*per_capita )

    
    
    
    popfactor = 1/Geo.get_PopCounties() if per_capita else 1.0
   

       # ------------------------- #
   
    ax1_1.set_ylabel("Total")
   

    x11, y11 = Cases.get_numbers_all_counties(f"total{data}",index_day=index_day)
    
    y11 = y11*popfactor
    
    if show_total:
        ax1_1.vlines(x11, np.zeros_like(y11), y11, linewidth=linewidth*2,
              label="Total", zorder=1, alpha=0.6, color = "chocolate")

    
    # -------------------------- #
    
    ax1_2.set_ylabel("New")
    
    x12, y12, label12 = Cases.get_numbers_all_counties_smooth(f"new{data}",
            index_day=index_day, window=window, polyord=polyord,
            time_frame=prevdays)

    
    y12 = y12*popfactor/prevdays

    if prevdays == 1:

        label12 = "Daily new" + label12

    elif prevdays > 1:

        label12 = f"Mean last {prevdays} days" + label12
   
    if show_mean:
        ax1_2.vlines(x12, np.zeros_like(y12), y12, linewidth=linewidth,
              label=label12, zorder=1, alpha=0.6)
    
   

    if per_capita:

        lim = quarantine_limit(show_countrylim,data,per_capita)
   
        if lim is not None:

            ax1_2.plot(ax1_2.get_xlim(), np.repeat(lim, 2), c="r", zorder=0,
                    lw=linewidth/2, label=f"Criterion {show_countrylim}")

    # ------------------- #
    
    
    ax1.plot(ax1.get_xlim(), [0, 0], c="gray", zorder=0, lw=linewidth/3)
    
    
    
    ym12, yM12 = extend_limits(minmax(y12), 0.07)
          # y12 can be negative

    ym12 = min(ym12, 0)



    for kwarg in ["name","code"]:

        county_index = Geo.get_county_index(**{kwarg:county})

        if county_index is not None:
        
            ax1_2.plot(np.repeat(county_index, 2), [ym12, yM12], c="crimson", zorder=0, lw=1.5 * linewidth, alpha=0.4)
    
            break 
    
    
    
    yM11 = extend_limits(minmax(y11), 0.07)[1]
          # y11 is only positive
    
    ym11 = yM11*ym12/(yM12+1e-20)
    
    ax1_2.set_ylim(ym12, yM12)
    ax1_1.set_ylim(ym11, yM11)
    
   
    xlim = extend_limits(minmax(np.append(x11,x12)),0.07)

    for (i, ax) in enumerate([ax1_1, ax1_2]):
   
        ax.set_xlim(xlim)
    
   
    ax1_2.legend(*collect_legends(ax1_1, ax1_2), loc=9)



    codes = np.array(Geo.get_CodeList(include_country=False))

    xt = np.array([int(x) for x in ax1.get_xticks() if 0<=int(x)<len(codes)])

    ax1.set_xticks(xt)

    ax1.set_xticklabels(codes[xt])
    
    

#===========================================================================#
#
# Adds to the pyqt figure specific sliders
#
#---------------------------------------------------------------------------#


    
def add_sliders(fig,cases,counties):

    fig.add_slider(label="Day", key="day", vs=cases.get_all_days(),
            v0=cases.get_dayindex(),next_row=True)

    fig.add_combobox(["infected","cured","deceased"], label="Data",
            key="data")

    fig.add_checkbox(label="Per capita", key="per")

    
    fig.add_combobox(["None","Switzerland","Germany"],label="Country limit",
            key="countrylim")
    
    fig.add_checkbox(label="Show new/mean", key="mean", status=True)

    fig.add_checkbox(label="Show total", key="total", status=True)
    
    fig.add_slider(label="Averaged days", key="prev", vs=np.arange(1, 30), v0=13, columnSpan=4)
    
    fig.add_slider(label="Smoothen", key="sg_w", vs=np.arange(1, 50, 2),
            columnSpan=5)
    
    fig.add_slider(label="Linewidth", key="lw", vs=np.linspace(0.5, 10, 20), v0=7, columnSpan=4)


def read_sliders(obj):

    return {    "data" : obj.get_combobox("data"),
           
                "day" : obj.get_slider("day"),

                "prevdays" : obj.get_slider("prev"),

                "per_capita": obj.get_checkbox("per"),
                
                "window" : obj.get_slider("sg_w"),

                "show_mean" : obj.get_checkbox("mean"),

                "show_total" : obj.get_checkbox("total"),

                "show_countrylim": obj.get_combobox("countrylim"),
                
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
             per_capita = True,
             show_mean = True,
             show_countrylim="DE",
             )
        
        
        fig.tight_layout()
        
        break
    
    plt.show()
    
    plt.close()
    


if __name__ == '__main__':

  desired_country = 'Romania'
  main(desired_country)

