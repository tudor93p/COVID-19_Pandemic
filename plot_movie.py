import matplotlib.pyplot as plt
import numpy as np
import os
import sys

from plot import plot

from utils import select_country_specific_objects

framerate = 10	# number of days/ movie second

start_padding = 6	# still frames at the beginning of the movies
end_padding = 14 	# still frames at the end of the movies




def main(country):
	cases, counties = select_country_specific_objects(country)
        
	start = 13


	def prefix_(task):
		showcases = task["showcases"]

		return counties.country_code+"_fig/"+showcases+"/"+showcases

	def fname_(task,i):

		return prefix_(task) + "_" + str(i+50).zfill(3)+".png"



	tasks =	[
		{"per_capita": True,
		"cmap": "cool",
		"showcases": "Total",
		"vminmax": [0, 25],  # vmax = (median + 2*standard dev)
		},
		
		{"per_capita": True,
		"cmap": "viridis",
		"showcases": "New",
		"vminmax": [0, 0.55],
		},
		]

	if len(sys.argv) > 1:
		try:	
			tasks = [tasks[i] for i in map(int, sys.argv[1: ]) if i in range(len(tasks))]
		except:
			pass
		 # in case sys.argv not provided or cannot be parsed to int


	for task in tasks:
		M = []

		prefix = prefix_(task)

		for i in cases.get_IndsDays()[start:]:


			fname = fname_(task,i)

			fig, axes = plt.subplots(1, 2, num=i, figsize=(10, 4.6))

			P = plot(
				axes,
				cases,
				counties,
				day=cases.get_Day(i),
				prevdays=7,
				show_mean=True,
				show_new=True,
				show_CHlim=False,
				linewidth=4.5,
				**task
				)

			M.append(P)

			fig.tight_layout()

			fig.savefig(fname, dpi=300, format="png")

			plt.close()

			print(task["showcases"], "-- done",i-start+1,"/",cases.get_iDay()-start+1)

#			break

		Data = np.max(M, axis=1)

		print("min max mean std median", np.round([f(Data) for f in [np.min, np.max, np.mean, np.std, np.median]], 3))

		print("max", np.round(np.max(Data), 3))

		print("median + 2*sigma", np.round(np.median(Data) + 2*np.std(Data), 3))

		print("mean + 2*sigma", np.round(np.mean(Data) + 2*np.std(Data), 3))

		print("median + sigma", np.round(np.median(Data) + 1*np.std(Data), 3))

		print("mean + sigma", np.round(np.mean(Data) + 1*np.std(Data), 3))

		print("\n")



		for i in range(1,start_padding+1):


			cmd = " ".join(["cp",fname_(task,start),fname_(task,start-i)])

			os.system(cmd)                       

		for i in range(1,end_padding+1):

			cmd = " ".join(["cp",fname_(task,cases.get_iDay()),fname_(task,i+cases.get_iDay())])


			os.system(cmd)


		

		cmd = "ffmpeg -y -f image2 -r "+str(framerate)+" -pattern_type glob -i '"+prefix+"_*.png' "+counties.country_code+"_fig/"+task["showcases"]+".mp4 "

		print(cmd)

		os.system(cmd)

		print()


if __name__ == "__main__":
	desired_country = 'Romania'
	main(desired_country)
