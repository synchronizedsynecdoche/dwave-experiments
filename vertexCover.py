# https://docs.ocean.dwavesys.com/en/stable/examples/min_vertex.html
import networkx as nx
import dwave_networkx as dnx
from neal import  SimulatedAnnealingSampler
s4 = nx.star_graph(4)
print(dnx.min_vertex_cover(nx.wheel_graph(5), SimulatedAnnealingSampler()))

