import matplotlib.pyplot as plt
import numpy as np
import os
import sys

import plot_newtotal_vsCounty, plot_newtotal_vsTime
import plot_vsCounty_vsTime, plot_map

from utils import select_country_specific_objects

framerate = 10	# number of days per movie second

start_padding = 6	# still frames at the beginning of the movies
end_padding = 14 	# still frames at the end of the movies




def main(country):
    cases, counties = select_country_specific_objects(country)
    
    start = 13

    folder0 = counties.country_code+"_fig/"
   
    def folder1(task):

        Q = task[0]["totalnew"] if "totalnew" in task[0].keys() else "both"

        return folder0 + task[0]["data"] + "-" + Q

    def prefix_(task):
    
        Q = task[0]["totalnew"] if "totalnew" in task[0].keys() else "both"

        return folder1(task) + "/" + task[0]["data"] + "-" + Q

    def fname_(task,i):
    
        return prefix_(task) + "_" + str(i+50).zfill(3)+".png"
    
    
    
    tasks = [[{ "data": "infected", "totalnew": tn,
                "per_capita": True, "prevdays": 14,
                "window":5},
  
                [10.5,5],       # figsize

                (121,plot_newtotal_vsTime,{"linewidth":4.5}),

                (122,plot_map,{"cmap" : cmap,
                            "vminmax" : [0, vM],
                            "show_colorbar":True}),

            ] for (cmap,tn,vM) in [("viridis","new",10),("cool","total",800)]

            ]+[
            [ { "data": "infected", 
                "per_capita": True, "prevdays": 14,
                "window":5},
  
                [8,5.7],        # figsize

                (224,plot_map,{"cmap" : "plasma", "totalnew": "new",
                            "vminmax" : [0, 10],
                            "show_colorbar":False,
                            "title" : "New"}),

                (211,plot_newtotal_vsTime,{"linewidth":3.7}),


                (223,plot_map,{"cmap" : "plasma", "totalnew": "total",
                            "vminmax" : [0, 800],
                            "show_colorbar":False,
                            "title" : "Total"}),



            ]]
    
    
    if len(sys.argv) > 1:
        try:
    	    tasks = [tasks[i] for i in map(int, sys.argv[1: ]) if i in range(len(tasks))]
        except:
            pass
    	 # in case sys.argv not provided or cannot be parsed to int
    
    
    for task in filter(lambda t:len(t)>0,tasks):
    
        prefix = prefix_(task)
  
        common_params,figsize,*subplots = task

        for i in cases.get_indices_all_days()[start:]:
    
            fname = fname_(task,i)
   
            print(i-start)

            plt.figure(num=i,figsize=figsize)
            for (ax,subplot,params) in subplots:

            
                plt.subplot(ax)
    
                subplot.plot(plt.gca(), cases, counties, day=cases.get_day(i),
                            **common_params, **params)
    
            plt.tight_layout()
            
            plt.savefig(fname, dpi=300, format="png")
            
            plt.close()
    
    
    
    
    
        for i in range(1,start_padding+1):
    
            cmd = " ".join(["cp",fname_(task,start),fname_(task,start-i)])
    
            os.system(cmd)
    
        for i in range(1,end_padding+1):
    
            cmd = " ".join(["cp", fname_(task, cases.get_dayindex()),
                fname_(task, i + cases.get_dayindex())])
    
    
            os.system(cmd)
    
    
    
    
        cmd = f"ffmpeg -y -f image2 -r {framerate} -pattern_type glob -i '{prefix}_*.png' {folder1(task)}.mp4"
    
        print(cmd)
    
        os.system(cmd)
    
        print()


if __name__ == "__main__":
    desired_country = 'Romania'
    main(desired_country)
