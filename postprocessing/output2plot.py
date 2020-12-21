import numpy as np
import re
from bokeh.io import output_file, show, export_png
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, FactorRange
from bokeh.layouts import column
import sys

INDICATOR = "DEBUG ArgMin State"
f = open(sys.argv[1])

generations = 0
branches = ["Blocking", "Tabu", "SA", "QA"]
data = {
         "Blocking" : [],
         "Tabu" : [],
         "SA" : [],
         "QA": []
            }
lines = f.readlines()
for line in lines:

    if INDICATOR in line:

        pure_idx = re.sub("[^0-9.\-]", "", line.split()[5])
        pure_value = re.sub("[^0-9.\-]", "", line.split()[6])
        data[branches[int(pure_idx)]].append(float(pure_value))
        if pure_idx == str(len(branches)-1):
            generations +=1
f.close()
generations = range(0,generations)
x = [(str(generation), branch) for generation in generations for branch in branches]
counts = sum(zip(data["Blocking"], data["Tabu"], data["SA"], data["QA"]), ())
source = ColumnDataSource(data=dict(x=x,counts=counts))

p = figure(x_range=FactorRange(*x), plot_height=250, plot_width=2000, title="Energies Found By Generation (Kerberos on Chimera)",
           toolbar_location="left")


p.vbar(x='x', top='counts', width=.85, source=source)
print(max(data["Blocking"]), min(data["Blocking"]))
p.y_range.end = 1
p.y_range.start =-2000 #min(data["Blocking"])# max(data["Blocking"])
p.xaxis.major_label_orientation = 1
p.xgrid.grid_line_color = None
q = figure(plot_width=2000, title="max-min within generation")
q.line(generations, [max(data["Blocking"][x], data["Tabu"][x], data["SA"][x], data["QA"][x]) - min(data["Blocking"][x], data["Tabu"][x], data["SA"][x], data["QA"][x])  for x in generations])
show(column(p,q))