import matplotlib.pyplot as plt
import numpy as np

from utils import POP_FACTOR,ASCII,quarantine_limit
from plot_utils import timestamp_to_date

#===========================================================================#
#
# Plotting function
#
#---------------------------------------------------------------------------#

def plot(ax2, Cases, Geo, totalnew, data, day=None, prevdays=7,
        per_capita=False, window=5, polyord=1, county_labels=True,
        county_capitals=False, cmap="viridis", vminmax=None,
        maxcolor=None,show_countrylim=None, show_colorbar=True,
        title=None,**kw):


    if day is None:
        day = Cases.get_day()	# the last day

    showncases = totalnew + " " + data

    totalnew, data = totalnew.lower(), data.lower()

    if title is None:

        print_day = timestamp_to_date(day,month="long")

        title = f"Nr. {showncases.lower()}: "

        title = title + f"{Geo.get_Name(ASCII=ASCII)}, {print_day}"
        

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
        
    cbarlabel = f"{label2} " + (f" (@ {POP_FACTOR} pop.)")*per_capita 

    Geo.plot(ax=ax2, column=showncases, cmap=cmap, zorder=0, 
            legend=show_colorbar,
            legend_kwds={'orientation':"horizontal", "pad":0.05,
                'label':cbarlabel},
            vmin=vmin, vmax=vmax)
       


        
    


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

    fig.add_checkbox(label="Show color bar", key="colorbar", status=True)


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

                "show_colorbar" : obj.get_checkbox("colorbar"),
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


        fig, axes = plt.subplots(1, 2, figsize=(9.5, 4.5))

        for (ax, cmap, new_total) in zip(axes,["YlGnBu",  "viridis"], ["New", "Total"]):
   
            
            P = plot(   ax,
                        cases,
                        counties,
                        new_total,
                        data,
                        prevdays=1,
                        per_capita = True,
                        cmap = cmap,
                        )
            
            
        fig.tight_layout()
            
        plt.show()
    
        plt.close()

    
        exit()    




if __name__ == '__main__':

    desired_country = 'Romania'
    main(desired_country)

