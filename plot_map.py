import matplotlib.pyplot as plt
import numpy as np

from utils import POP_FACTOR,ASCII,quarantine_limit
from plot_utils import timestamp_to_date,make_title

#===========================================================================#
#
# Plotting function
#
#---------------------------------------------------------------------------#

def plot(ax2, Cases, Geo, totalnew, data, day=None, prevdays=7,
        per_capita=False, window=5, polyord=1, county_labels=True,
        county_capitals=False, cmap="viridis", vminmax=None,
        maxcolor=None,show_countrylim=None, cbarlabel=None, title=None,**kw):


    if day is None:
        day = Cases.get_day()	# the last day

    totalnew, data = totalnew.lower(), data.lower()

    showncases = totalnew + " " + data


    title = make_title(
                "Nr. showncases in county on day" if title is None else title,
                totalnew=totalnew,
                popfactor=(f"@ {POP_FACTOR} pop.")*per_capita,
                data=data,
                showncases=showncases,
                county=Geo.get_Name(ASCII=ASCII),
                day=timestamp_to_date(day,month="long"),
                )

    if title is not None:
        ax2.set_title(title)
        








                                    




 # ------------------------- #

   

    for cc in Geo.get_CodeList(include_country=False):
  
        pop = Geo.get_Pop(code=cc)

        nr = 1/pop if per_capita else 1 


        if "total" == totalnew:
        
            nr *= Cases.get_number(showncases, day=day, county=cc)
        
            label2 = "Cummulated cases"
        
        elif "new" == totalnew:
        
            y2,label2 = Cases.get_number_smooth(
                            showncases, day=day,
                            window=window, polyord=polyord,
                            time_frame=prevdays, county=cc)
            
            if prevdays==1:
                label2 = "Daily new" + label2
                
            elif prevdays>1:
                label2 = f"Mean last {prevdays} days" + label2

            nr *= y2/prevdays
            
            lim = quarantine_limit(show_countrylim,data,per_capita,pop)
            
            if lim is not None:

                nr = float(nr>lim)

                label2 = label2 + " > criterion " + show_countrylim 

                vminmax = [0,1]

                maxcolor = 1

        Geo.set_geoColumn(showncases, nr, code=cc)
        
        if county_labels:
        
            xy, kwargs = Geo.get_countyPlotLabel(code=cc)
        
            if xy is not None:
                ax2.text(*xy, str(cc), **kwargs, zorder=4, color="k" if cmap in ["cool", "PuBuGn", "YlGnBu", "Spectral", "coolwarm"] else "w")
            

    if county_capitals:
        ax2.scatter(*Geo.get_geoCapCoord_All().T, c='r', s=2, zorder=2)
    
    
    xlim, ylim = Geo.get_geoCountryBox()
    
    ax2.set_xlim(xlim)
    ax2.set_ylim(ylim)
    
    ax2.set_axis_off()
    
    if vminmax is None:
        vmin = 0
        vmax = np.max(Geo.get_geoColumn(showncases))
    
    else:
        vmin, vmax = vminmax
    
    if maxcolor is not None:
            vmax *= maxcolor
        
    cbarlabel = make_title(
        "label2 popfactor" if cbarlabel is None else cbarlabel,
        label2=label2,
        popfactor=(f"@ {POP_FACTOR} pop.")*per_capita,
        totalnew=totalnew,
        data=data,
        showncases=showncases,
        county=Geo.get_Name(ASCII=ASCII),
        day=timestamp_to_date(day,month="short")
                 )


#    Geo.plot_custom(ax2,   # only this takes into account 'divider_kwargs'
    Geo.plot(ax2,
            divider_kwargs =
            {
            "position":     "right",
            "size":         "4%",
            "pad":          "1%",
            },
            legend_kwds={
            **({"label":    cbarlabel} if cbarlabel is not None else {}),
            "pad":          0.08,
            "fraction":     0.03,
#            "orientation":  "horizontal",
            "orientation":  "vertical",
            },
            column=showncases, cmap=cmap, zorder=0, vmin=vmin, vmax=vmax,
            legend=True,
            )
        
    


#===========================================================================#
#
# Adds to the pyqt figure specific sliders and reads them
#
#---------------------------------------------------------------------------#


    
def add_sliders(fig,cases,counties):


    fig.add_slider(label="Day", key="day", vs=cases.get_all_days(),
            v0=cases.get_dayindex(),next_row=True)

    fig.add_combobox(["Total", "New"], label="Total/New", key="totalnew")

    fig.add_combobox(["infected","cured","deceased"], label="Data",
            key="data")


    fig.add_checkbox(label="Per capita", key="per")


    fig.add_combobox(["None","Switzerland","Germany"],label="Country limit", key="countrylim" )
    
    
    fig.add_slider(label="Averaged days", key="prev", vs=np.arange(1, 30), v0=13, columnSpan=4)
    
    fig.add_slider(label="Smoothen", key="sg_w", vs=np.arange(1, 50, 2), columnSpan=5 )
    


    fig.add_combobox(["PuBuGn", "cool", "YlGnBu", "plasma", "coolwarm",
        "Spectral", "viridis"], label="Color map", key="cmap" )
    
    fig.add_slider(label="Saturation", key="maxcolor", vs=np.linspace(1e-4, 1,
        71), v0=70, columnSpan=5)
    
    fig.add_checkbox(label="County labels", key="codes", status=True)

    fig.add_checkbox(label="County capitals", key="capitals", status=False)



def read_sliders(obj):

    return {    "totalnew" : obj.get_combobox("totalnew"),
    
                "data" : obj.get_combobox("data"),
            
                "per_capita": obj.get_checkbox("per"),
                
                "show_countrylim": obj.get_combobox("countrylim"),
                
                "prevdays" : obj.get_slider("prev"),
                
                "window" : obj.get_slider("sg_w"),
                
                "day" : obj.get_slider("day"),
                
                "cmap" : obj.get_combobox("cmap"),
                
                "maxcolor" : obj.get_slider("maxcolor"),
                
                "county_labels": obj.get_checkbox("codes"),
            
                "county_capitals" : obj.get_checkbox("capitals"),

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

        for (ax, cmap, new_total) in zip([axes],["YlGnBu",  "viridis"], ["New", "Total"]):
   
            
            P = plot(   ax,
                        cases,
                        counties,
                        new_total,
                        data,
                        prevdays=1,
                        per_capita = True,
                        cmap = cmap,
#                        title = "data",
#                        cbarlabel = "totalnew day popfactor",
                        )
            
            
        fig.tight_layout()
            
        plt.show()
    
        plt.close()

    
        exit()    




if __name__ == '__main__':

    desired_country = 'Romania'
    main(desired_country)

