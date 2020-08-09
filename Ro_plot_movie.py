from Ro_plot import *

import os



for (cmap,cases) in zip(["YlGnBu", "viridis"],["New","Total"]):

  M = []

  prefix = "Ro_fig/"+cases+"/"+cases

  for i in Cases.get_IndsDays()[::-1]:

    fname = prefix + "_" + str(i).zfill(3)+".png"

    fig,axes = plt.subplots(1,2,num=i,figsize=(10,4))
  
    P = plot(
      	axes,
      	per_capita=True,
      	day = Cases.get_Day(i),
      	cases = cases,
      	cmap = cmap,
      	show_mean = True,
      	show_new = True,
      	show_CHlim = False,
      	linewidth = 2.5
      	)

    M.append(P)

    fig.tight_layout()
  
    fig.savefig(fname,dpi=300,format="png")
  
    plt.close()

    print(cases,cmap,i)

#    break

  print(cases,cmap,np.max(M,axis=0))

  print("\n")

  cmd = "ffmpeg -y -f image2 -r 8 -pattern_type glob -i '"+prefix+"_*.png' Ro_fig/"+cases+".mp4 "

  print(cmd)

  os.system(cmd)

  print()

