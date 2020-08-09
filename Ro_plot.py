import numpy as np
from scipy.signal import savgol_filter
import matplotlib.pyplot as plt
import Ro_datelazi,Ro_counties

Cases = Ro_datelazi.RoCases("Ro_data/date_09_august_la_13_00.json")

PopFactor = 100000

Geo = Ro_counties.Counties(PopFactor=PopFactor)


def extend_limits(lim,amount=0.04):

  return np.array(lim) + np.diff(lim)*np.array([-1,1])*amount

def minmax(A):

  return np.array([np.min(A),np.max(A)])



def plot(axes,county="România",day=Cases.get_Day(),cmap="viridis",window=5,polyord=1,prevdays=14,per_capita=False,show_mean=True,show_CHlim=False,show_new=True,cases="Total",linewidth=2.5):


  ax1,ax2 = axes

  ax1.set_xlabel("Day index")

  ax1_1 = ax1.twinx()
  ax1_2 = ax1


  for ax in [ax1_1,ax1_2]:
    ax.ticklabel_format(axis='y',style='sci',scilimits=(-2,2))


  ax1.set_title(county + (" (@ "+str(PopFactor)+" pop.)")*per_capita)


  countycode = Geo.get_Code(name=county)

 
  popfactor = 1/Geo.get_Pop(code=countycode) if per_capita else 1

 # ------------------------- #

  ax1_1.set_ylabel("Total cases")

  x11,y11 = Cases.Nr_Infected_AllDays(County=countycode)

  y11 = y11*popfactor

  ax1_1.plot(x11,y11,label="Total",c='orange',lw=linewidth)


  # -------------------------- #

  ax1_2.set_ylabel("New cases")

  x12,y12 = Cases.Nr_NewInfected_AllDays(County=countycode)

  y12 *= popfactor

  if show_new:
    ax1_2.vlines(x12,np.zeros_like(y12),y12,linewidth=linewidth/2,label="Daily new",zorder=1)

 

  x14,y14 = Cases.Nr_NewInfected_AllDays(TimeFrame=prevdays,County=countycode)
  
  y14 *= popfactor/prevdays
  

  label14="Daily new" if prevdays==1 else "Mean last "+str(prevdays)+" days"


  if window!=1 and polyord!=0:

    y14 = savgol_filter(y14,window,polyord) 

    label14 = label14 + " (smooth)"

  if show_mean:
    ax1_2.plot(x14,y14,label=label14,c='royalblue',lw=linewidth,zorder=5)


  if show_CHlim:
    CH_lim = Geo.get_Pop(code=countycode)*PopFactor/100000*(60/14)*popfactor

    ax1_2.plot(ax1_2.get_xlim(),np.repeat(CH_lim,2),c="r",zorder=0,lw=linewidth/2,label="Criterion CH")


  # ------------------- #

   
  ax1.plot(ax1.get_xlim(),[0,0],c="gray",zorder=0,lw=linewidth/3)

  ym12,yM12 = extend_limits(minmax(y12),0.07)
	# y12 can be negative 
  ym12 = min(ym12,0)

  ax1.plot(np.repeat(Cases.get_iDay(day),2),[ym12,yM12],c="pink",zorder=0,lw=2*linewidth)





  yM11 = extend_limits(minmax(y11),0.07)[1]
	# y11 is only positive
  
  ym11 = yM11*ym12/yM12

  ax1_2.set_ylim(ym12,yM12)
  ax1_1.set_ylim(ym11,yM11)



  for (i,ax) in enumerate([ax1_1,ax1_2]):
    ax.legend(loc=2-i)
  
    ax.set_xlim(0,np.max(np.append(x11,x12))+2)



  # ----------------- #


  for cc in Geo.get_CodeList(RO=False):
  
    if cases == "Total":

      tot = Cases.Nr_Infected(Day=day,County=cc)

      Geo.set_geoColumn(cases,tot*popfactor,code=cc)

      label2 = "Total cases"

  


    elif cases == "New":

      label2 = "Daily new" if prevdays==1 else "Mean last "+str(prevdays)+" days"
      if window!=1 and polyord!=0:
  
        y2 = Cases.Nr_NewInfected_AllDays(TimeFrame=prevdays,County=cc)[1]
  
        new = savgol_filter(y2,window,polyord)[Cases.get_iDay(day)]
   
        label2 = label2 + " (smooth)"
   
      else:
      
        new = Cases.Nr_NewInfected(Day=day,TimeFrame=prevdays,County=cc)


      Geo.set_geoColumn(cases,new*popfactor/prevdays,code=cc)


    ax2.text(*Geo.get_geoCenter(code=cc)[::-1],str(cc),verticalalignment='center',horizontalalignment='center',zorder=2)


  ax2.set_xticks([])
  ax2.set_yticks([])
  ax2.set_xlabel("")
  ax2.set_ylabel("")


  vmax = np.max(Geo.get_geoColumn(cases))

#  if per_capita: vmax = 0.76867179 if cases=="New" else 36.74454751
#  else: vmax = 153.171428   if cases=="New" else 7322
 

  Geo.plot(ax=ax2,column=cases,cmap=cmap,zorder=0,legend=True,legend_kwds={'orientation':"horizontal","pad":0.05,'label':" ".join([day+":",label2]+[" (@ "+str(PopFactor)+" pop.)"]*per_capita)},vmin=0,vmax=vmax)



  return [np.max(Geo.get_geoColumn(cases,code="SV",complement=C)) for C in [False,True]]





if __name__ == '__main__':

  for (cmap,cases) in zip(["YlGnBu", "viridis"],["New","Total"]):


    fig,axes = plt.subplots(1,2,figsize=(10,4))
    
    plot(
      	axes,
      	per_capita=True,
      	day = Cases.get_Day(),
      	cases = cases,
      	cmap = cmap,
      	show_mean = True,
      	show_new = True,
      	show_CHlim = True,
      	)


    fig.tight_layout()
    
  plt.show()
    
  plt.close()


