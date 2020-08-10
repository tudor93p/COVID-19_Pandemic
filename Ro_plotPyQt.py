import PlotPyQt
from RO_plot import *

def funfig(obj,fig,axes): 

  plot(
    axes,
    per_capita=obj.get_checkbox("per"),
    county = obj.get_combobox("county"),
    day = obj.get_slider("day"),
    cases = obj.get_combobox("cases"),
    cmap = obj.get_combobox("cmap"),
    window = int(obj.get_slider("sg_w")),
    prevdays = int(obj.get_slider("prev")),
    show_mean = obj.get_checkbox("mean"),
    show_new = obj.get_checkbox("new"),
    show_CHlim = obj.get_checkbox("CHlim"),
    linewidth = obj.get_slider("lw")
    )


Fig = PlotPyQt.Figure(funfig,1,2,figsize=(10,4))#,tight=True,**kwargs) 




Fig.add_slider(label="Smoothen",key="sg_w",vs=np.arange(1,50,2))#,columnSpan=1,next_row=True)

Fig.add_slider(label="Average previous days",key="prev",vs=np.arange(1,30),v0=13)#,columnSpan=1,next_row=True)

#Fig.add_slider(label="Poly order",key="sg_o",vs=range(30))#,columnSpan=1,next_row=True)

Fig.add_slider(label="Day",key="day",vs=Cases.get_Days(),v0=Cases.get_iDay())






Fig.add_combobox(Geo.CountyNames(RO=True),label="County",key="county",columnSpan=1)#,next_row=False)




Fig.add_checkbox(label="Show new",key="new",next_row=False,vdiv=True,columnSpan=1,status=True)

Fig.add_checkbox(label="Show mean",key="mean",next_row=False,vdiv=True,columnSpan=1,status=True)

Fig.add_checkbox(label="Criterion CH",key="CHlim",next_row=False,vdiv=True,columnSpan=1,status=False)


Fig.add_checkbox(label="Per capita",key="per",next_row=True,vdiv=False,columnSpan=1)
Fig.add_combobox(["Total","New"],label="Color",key="cases",next_row=False,columnSpan=1,vdiv=True)

Fig.add_combobox(["PuBuGn","cool","YlGnBu","plasma","coolwarm","Spectral","viridis"],label="Color map",key="cmap",next_row=False,columnSpan=1,vdiv=True)

Fig.add_slider(label="Linewidth",key="lw",vs=np.linspace(0.5,10,20),v0=5,next_row=False,vdiv=True,columnSpan=4)

Fig.show()


