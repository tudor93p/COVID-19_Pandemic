import numpy as np

import python_libraries.PlotPyQt as PlotPyQt

from plot import plot
from utils import select_country_specific_objects, ASCII




def main(country):
  cases, counties = select_country_specific_objects(country)

  def funfig(obj, fig, axes):

    plot(
      axes,
      cases,
      counties,
      per_capita=obj.get_checkbox("per"),
      county=obj.get_combobox("county"),
      day=obj.get_slider("day"),
      showcases=obj.get_combobox("cases"),
      cmap=obj.get_combobox("cmap"),
      window=obj.get_slider("sg_w"),
      prevdays=obj.get_slider("prev"),
      show_mean=obj.get_checkbox("mean"),
      show_new=obj.get_checkbox("new"),
      show_CHlim=obj.get_checkbox("CHlim"),
      linewidth=obj.get_slider("lw"),
      maxcolor=obj.get_slider("maxcolor"),
      county_labels=obj.get_checkbox("codes"),
      county_capitals=obj.get_checkbox("capitals"),
      )

  fig = PlotPyQt.Figure(funfig, 1, 2, figsize=(10, 4.6))#, tight=True, **kwargs)

  fig.add_combobox(counties.CountyNames(include_country=True,ASCII=ASCII), label="County", key="county", columnSpan=1)#, next_row=False)

  #Fig.add_slider(label="Poly order", key="sg_o", vs=range(30))#, columnSpan=1, next_row=True)

  fig.add_checkbox(label="Per capita", key="per", next_row=False, vdiv=False, columnSpan=1)

  fig.add_checkbox(label="Show new", key="new", next_row=False, vdiv=False, columnSpan=1, status=True)

  fig.add_checkbox(label="Criterion CH", key="CHlim", next_row=False, vdiv=False, columnSpan=1, status=False)

  fig.add_slider(label="Linewidth", key="lw", vs=np.linspace(0.5, 10, 20), v0=7, next_row=False, vdiv=True, columnSpan=4)

  fig.add_checkbox(label="Show mean", key="mean", next_row=True, vdiv=False, columnSpan=1, status=True)

  fig.add_slider(label="Averaged days", key="prev", vs=np.arange(1, 30), v0=13, next_row=False, columnSpan=4)

  fig.add_slider(label="Smoothen", key="sg_w", vs=np.arange(1, 50, 2), next_row=False, columnSpan=5, vdiv=False)

  fig.add_slider(label="Day", key="day", vs=cases.get_Days(), v0=cases.get_iDay(), next_row=True)

  fig.add_combobox(["Total", "New"], label="Color", key="cases", next_row=True, columnSpan=1, vdiv=False)

  fig.add_combobox(["PuBuGn", "cool", "YlGnBu", "plasma", "coolwarm", "Spectral", "viridis"], label="Color map", key="cmap", next_row=False, columnSpan=1, vdiv=False)

  fig.add_slider(label="Saturation", key="maxcolor", vs=np.linspace(1e-4, 1, 41), v0=40, next_row=False, vdiv=False, columnSpan=5)

  fig.add_checkbox(label="County labels", key="codes", next_row=False, vdiv=False, columnSpan=1, status=True)
  fig.add_checkbox(label="County capitals", key="capitals", next_row=False, vdiv=False, columnSpan=1, status=False)

  fig.show()


if __name__ == "__main__":
  desired_country = 'Romania'
  main(desired_country)
