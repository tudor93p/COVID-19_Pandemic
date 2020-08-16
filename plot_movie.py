import matplotlib.pyplot as plt
import numpy as np
import os
import sys

from plot import plot

from utils import select_country_specific_objects


def prefix_(task):
	cases = task["cases"]
	return "Ro_fig/"+cases+"/"+cases


def main(country):
	cases, _ = select_country_specific_objects(country)

	task1 = {"per_capita": True,
		"cmap": "cool",
		"cases": "Total",
		"vminmax": [0, 25],  # vmax = (median + 2*standard dev)
		}

	task2 = {"per_capita": True,
		"cmap": "viridis",
		"cases": "New",
		"vminmax": [0, 0.55],
		}

	tasks = [task1, task2]

	if len(sys.argv) > 1:
		tasks = [tasks[i] for i in map(int, sys.argv[1: ]) if i in range(len(tasks))]


	for task in tasks:
		M = []

		prefix = prefix_(task)

		for i in cases.get_IndsDays()[13: ]:

			fname = prefix + "_" + str(i).zfill(3)+".png"

			fig, axes = plt.subplots(1, 2, num=i, figsize=(10, 4.6))

			P = plot(
				axes,
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

			print(task["cases"], i)

		Data = np.max(M, axis=1)

		print("min max mean std median", np.round([f(Data) for f in [np.min, np.max, np.mean, np.std, np.median]], 3))

		print("max", np.round(np.max(Data), 3))

		print("median + 2*sigma", np.round(np.median(Data) + 2*np.std(Data), 3))

		print("mean + 2*sigma", np.round(np.mean(Data) + 2*np.std(Data), 3))

		print("median + sigma", np.round(np.median(Data) + 1*np.std(Data), 3))

		print("mean + sigma", np.round(np.mean(Data) + 1*np.std(Data), 3))

		print("\n")

		cmd = "ffmpeg -y -f image2 -r 8 -pattern_type glob -i '"+prefix+"_*.png' Ro_fig/"+task["cases"]+".mp4 "

		print(cmd)

		os.system(cmd)

		print()


if __name__ == "__main__":
	desired_country = 'Romania'
	main(desired_country)
