# modified from code at https://docs.ocean.dwavesys.com/en/stable/examples/map_coloring_full_code.html
'''
 instead of determining what the 4-coloring of a map is (which exists),
 determine if a given graph is 3-colorable, and if so, generate a solution
'''
import dwavebinarycsp
from neal import  SimulatedAnnealingSampler
import networkx as nx
import matplotlib.pyplot as plt

provinces = ['AB', 'BC', 'MB', 'NB', 'NL', 'NS', 'NT', 'NU', 'ON', 'PE', 'QC', 'SK', 'YT']
neighbors = [('AB', 'BC'), ('AB', 'NT'), ('AB', 'SK'), ('BC', 'NT'), ('BC', 'YT'), ('MB', 'NU'),
             ('MB', 'ON'), ('MB', 'SK'), ('NB', 'NS'), ('NB', 'QC'), ('NL', 'QC'), ('NT', 'NU'),
             ('NT', 'SK'), ('NT', 'YT'), ('ON', 'QC')]

def not_both_1(v, u):
    return not (v and u)
def plot_map(sample):
    G = nx.Graph()
    G.add_nodes_from(provinces)
    G.add_edges_from(neighbors)
    # Translate from binary to integer color representation
    color_map = {}
    for province in provinces:
          for i in range(colors):
            if sample[province+str(i)]:
                color_map[province] = i
    # Plot the sample with color-coded nodes
    node_colors = [color_map.get(node) for node in G.nodes()]
    nx.draw_circular(G, with_labels=True, node_color=node_colors, node_size=3000, cmap=plt.cm.rainbow)
    plt.savefig("out.png")
one_hot_encoding = {(0,0,1), (0,1,0), (1,0,0)}
colors = len(one_hot_encoding)
csp = dwavebinarycsp.ConstraintSatisfactionProblem(dwavebinarycsp.BINARY)

for province in provinces:
    variables = [province+str(i) for i in range(colors)]
    csp.add_constraint(one_hot_encoding, variables)
for neighbor in neighbors:
    v, u = neighbor
    for i in range(colors):
        variables = [v+str(i), u+str(i)]
        csp.add_constraint(not_both_1, variables)
bqm = dwavebinarycsp.stitch(csp)

sampleset = SimulatedAnnealingSampler().sample(bqm, num_reads=1000)
sample = sampleset.first.sample
if not csp.check(sample):
    print("Likely not 3-colorable")
else:
    plot_map(sample)
    