import matplotlib.pyplot as plt
import numpy as np

import matplotlib.ticker as ticker


from utils import POP_FACTOR,ASCII,quarantine_limit

from plot_utils import mgrid_from_1D,extend_limits
from plot_utils import make_title,timestamp_to_date





#===========================================================================#
#
# Plotting function
#
#---------------------------------------------------------------------------#



def plot(ax1, Cases, Geo, totalnew, data, day=None, county=None, prevdays=7,
        per_capita=False, window=5, polyord=1, show_countrylim=None, 
        title=None, cmap="viridis", vminmax=None, maxcolor=None, 
        cbarlabel=None, **kw):


    totalnew,data = totalnew.lower(), data.lower()
    
    ax1.set_ylabel("County")
    
    showncases = totalnew + " " + data


    title = make_title(
        "Nr. showncases in county popfactor" if title is None else title,
        totalnew=totalnew,
        popfactor=(f"@ {POP_FACTOR} pop.")*per_capita,
        data=data,
        showncases=showncases,
        county=Geo.get_Name(ASCII=ASCII),
        )

    if title is not None:
        ax1.set_title(title)
    
    
    populations = Geo.get_PopCounties()
    codes = np.array(Geo.get_CodeList(include_country=False))
    

    x,y,Z,lab = Cases.get_numbers_all_days_all_counties_smooth(showncases,window=window,polyord=polyord,time_frame=prevdays)


    if "total" in totalnew:

        lab = "Total nr." + lab

    elif prevdays == 1:

        lab = "Daily new" + lab

    elif prevdays > 1:

        lab = f"Mean last {prevdays} days " + lab

        Z /= prevdays

    if per_capita:

        Z /= populations

    criterion_applied = False

    for (cj,(cc,cp)) in enumerate(zip(codes,populations)):

        clim = quarantine_limit(show_countrylim,data,per_capita,cp)

        if clim is not None:

            criterion_applied = True

            Z[:,cj] = Z[:,cj] > clim

            vminmax = [0,1]

            maxcolor = 1

    if criterion_applied:
        lab = lab + " > criterion " + show_countrylim 

    if vminmax is None:
        vmin,vmax = 0, np.max(Z)

    else:
        vmin, vmax = vminmax
    
    if maxcolor is not None:
        vmax *= maxcolor


    P = ax1.pcolormesh(*mgrid_from_1D(x,y), Z, cmap=cmap, edgecolors='face',
                vmax=vmax,vmin=vmin,zorder=5)

    cbarlabel = make_title(
                "lab" if cbarlabel is None else cbarlabel,
                lab=lab,
                totalnew=totalnew,
                popfactor=(f"@ {POP_FACTOR} pop.")*per_capita,
                data=data,
                showncases=showncases,
                county=Geo.get_Name(ASCII=ASCII),
                )

    sfmt = ticker.ScalarFormatter(useMathText=False) 
    sfmt.set_powerlimits((0, 0))
    
    cbar = ax1.get_figure().colorbar(P, ax=ax1, boundaries=np.linspace(vmin,
        vmax,100), ticks=[vmin,vmax], format=sfmt)
    
    if cbarlabel is not None:
        cbar.set_label(cbarlabel,rotation=90)



    ylim = extend_limits(ax1.get_ylim(),0.01)
        
    xlim = extend_limits(ax1.get_xlim(),0.01)

    if day is not None:

        ax1.plot(np.repeat(Cases.get_dayindex(day) + 0.5, 2), ylim, c="crimson",
                zorder=8, lw=1, alpha=0.5)


    for kwarg in ["name","code"]:

        county_index = Geo.get_county_index(**{kwarg:county})

        if county_index is not None:

            ax1.plot(xlim, np.repeat(county_index + 0.5, 2), c="crimson", zorder=8,
                    lw=1, alpha=0.5)
    
            break 

    xt = np.array([int(x) for x in ax1.get_xticks() if
        0<=int(x)<=Cases.get_dayindex()])

    ax1.set_xticks(xt)
    ax1.set_xticklabels([timestamp_to_date(Cases.get_day(x)) for x in xt])

    yt = np.array([int(y) for y in ax1.get_yticks() if 0<=int(y)<len(codes)])

    ax1.set_yticks(yt)

    ax1.set_yticklabels(codes[yt])



    ax1.set_ylim(ylim)
    ax1.set_xlim(xlim)

#===========================================================================#
#
# Adds to the pyqt figure specific sliders
#
#---------------------------------------------------------------------------#


    
def add_sliders(fig,cases,counties):

    fig.add_combobox(["Total", "New"], label="Total/New", key="totalnew")

    fig.add_combobox(["infected","cured","deceased"], label="Data",
            key="data")

    fig.add_checkbox(label="Per capita", key="per" )

    fig.add_combobox(["None","Switzerland","Germany"],label="Country limit", key="countrylim" )
    
    
    fig.add_slider(label="Averaged days", key="prev", vs=np.arange(1, 30), v0=13, columnSpan=4)
    
    fig.add_slider(label="Smoothen", key="sg_w", vs=np.arange(1, 50, 2),  columnSpan=5 )
    
    fig.add_combobox(["PuBuGn", "cool", "YlGnBu", "plasma", "coolwarm",
        "Spectral", "viridis"], label="Color map", key="cmap" )
    
    fig.add_slider(label="Saturation", key="maxcolor", vs=np.linspace(1e-4, 1,
        71), v0=70, columnSpan=5)



def read_sliders(obj):

    return {    "totalnew" : obj.get_combobox("totalnew"),

                "data" : obj.get_combobox("data"),
           
                "per_capita": obj.get_checkbox("per"),

                "show_countrylim": obj.get_combobox("countrylim"),

                "prevdays" : obj.get_slider("prev"),

                "window" : obj.get_slider("sg_w"),

                "cmap" : obj.get_combobox("cmap"),

                "maxcolor" : obj.get_slider("maxcolor"),
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
             "new",
             data,
             per_capita = False,#True,
             show_mean = True,
             show_new = True,
#             show_countrylim="DE",
#            cbarlabel="data",
#            title="in county"
             )
        
        
        fig.tight_layout()
        
        break
    
    plt.show()
    
    plt.close()
    


if __name__ == '__main__':

  desired_country = 'Romania'
  main(desired_country)

