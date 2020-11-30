import numpy as np

import python_libraries.PlotPyQt as PlotPyQt

import plot_newtotal_vsTime,plot_newtotal_vsCounty,plot_map
import plot_vsCounty_vsTime

from utils import select_country_specific_objects, ASCII


subplots = [plot_newtotal_vsTime, plot_newtotal_vsCounty,
                        plot_vsCounty_vsTime,plot_map]
nrows,ncols = 2,2

subplots = [plot_vsCounty_vsTime,plot_newtotal_vsTime]
nrows,ncols=1,2

subplots = [plot_newtotal_vsTime, plot_map]
nrows,ncols=1,2



def main(country):
    cases, counties = select_country_specific_objects(country)
    
    def funfig(obj, fig, axes):
  
        kwargs = subplots[0].read_sliders(obj)
        
        for subplot in subplots[1:]:

            kwargs.update(subplot.read_sliders(obj))


        if len(subplots)==1:
            axes=[axes]
        else:
            axes=np.reshape(axes,-1)

        for (subplot,ax) in zip(subplots,axes):

            subplot.plot(
                ax,
                cases,
                counties,
                **kwargs
                )
            
            


    fig = PlotPyQt.Figure(funfig, nrows,ncols, figsize=(5*ncols, 4.5*nrows),
                )#, tight=True, **kwargs)
    
    for subplot in subplots:

        subplot.add_sliders(fig,cases,counties)

    
    fig.show()
    

if __name__ == "__main__":
    desired_country = 'Romania'
    main(desired_country)
