import numpy as np
from datetime import datetime
import pandas as pd

def extend_limits(lim, amount=0.04):

    return np.array(lim) + np.diff(lim)*np.array([-1, 1])*amount

def minmax(A):

    return np.array([np.min(A), np.max(A)])



def collect_legends(*axes):

    lines, labels = axes[0].get_legend_handles_labels()

    for ax in axes[1:]:

        li, la = ax.get_legend_handles_labels()

        lines = lines + li
        labels = labels + la


    return lines,labels




def mgrid_from_1D(x,y,extend=False):

  if extend:
    x,y = [np.append(a,a[-1] + np.mean(np.diff(a))) for a in [x,y]]
                # otherwise pcolormesh ignores last row and column of Z

  X = np.repeat(np.reshape(x,(-1,1)),len(y),axis=1)

  Y = np.repeat(np.reshape(y,(1,-1)),len(x),axis=0)

  return X,Y



def timestamp_to_date(ts,month="short"):
    d = pd.Timestamp(ts).date()

    # silly way -- the implicit functions seem to output German months
    #               and I didn't manage to locale.setlocale(LC_TIME ...)


    if month =="short":
        
        en_mo = ["Jan", "Feb", "Mar", "Apr", "May", "June", "July", "Aug", "Sept", "Oct", "Nov", "Dec"]


        return str(d.day) + " " + en_mo[d.month-1]


    else:
        en_mo = ["January", "February", "March", "April", "May", "June",
                "July", "August", "September", "October", "November",
                "December"]


        return  en_mo[d.month-1] + " " + str(d.day)








