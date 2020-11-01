import dwavebinarycsp
from neal import SimulatedAnnealingSampler
from dwave.system import DWaveSampler, EmbeddingComposite
import networkx as nx
import matplotlib.pyplot as plt
from datetime import datetime
import pickle


def backup(expName, samples):

    with open("data/"+expName + str(datetime.now()), "wb") as f:
                
            pickle.dump(samples, f)

wa_out = "{2, 3, 4, 5} | {1, 3} | {1, 2, 5, 31, 32} | {1, 5, 6, 7} | {1, 3, 4, 6, 8, 27, 31, 42} | {4, 5, 7, 8, 9, 10} | {4, 6, 10} | {5, 6, 9, 18, 19, 33, 34, 42} | {6, 8, 10, 13, 17, 18} | {6, 7, 9, 13} | {12, 13, 14, 15} | {11, 14, 16} | {9, 10, 11, 17} | {11, 12, 15, 16, 38} | {11, 14, 17, 20, 38} | {12, 14, 38, 40} | {9, 13, 15, 18, 19, 20} | {8, 9, 17, 19} | {8, 17, 18, 20, 33, 36} | {15, 17, 19, 36, 38, 39} | {22, 23, 24} | {21, 23, 24, 46, 47} | {21, 22, 29, 30, 47} | {21, 22} | {26, 27} | {25, 27, 28, 30, 45} | {5, 25, 26, 31, 42, 45} | {26, 29, 30} | {23, 28, 30} | {23, 26, 28, 29, 44, 45} | {3, 5, 27, 32} | {3, 31} | {8, 19, 34, 35, 36, 37} | {8, 33, 37, 41, 42} | {33, 36, 37, 49} | {19, 20, 33, 35, 39, 49} | {33, 34, 35, 43} | {14, 15, 16, 20, 39, 40} | {20, 36, 38, 49} | {16, 38} | {34, 42, 43, 44} | {5, 8, 27, 34, 41, 44, 45} | {37, 41, 44} | {30, 41, 42, 43, 45} | {26, 27, 30, 42, 44} | {22, 47, 48} | {22, 23, 46} | {46} | {35, 36, 39}".replace(" ","")
wa_singlets = wa_out.split("|")
cleaned = []

for singlet in wa_singlets:
    cleaned.append(singlet.replace("{","").replace("}","").split(","))
#print(cleaned)

vertices = []
for i in range(1,len(wa_singlets)+1):
    vertices.append(str(i))

#print(vertices)

edges = []

for i in range(0, len(cleaned)):
    for j in range(len(cleaned[i])):
        edges.append((str(i+1), cleaned[i][j]))


#print(edges)

def not_same_color(v,u):
    return not (v and u)


one_hot_encoding = {(0,0,0,1), (0,0,1,0), (0,1,0,0), (1,0,0,0)}
colors = len(one_hot_encoding)

def plot_map(sample):
    G = nx.Graph()
    G.add_nodes_from(vertices)
    G.add_edges_from(edges)
    # Translate from binary to integer color representation
    color_map = {}
    for state in vertices:
          for i in range(colors):
            if sample[state+"_"+str(i)]:
                color_map[state] = i
    # Plot the sample with color-coded nodes
    node_colors = [color_map.get(node) for node in G.nodes()]
    nx.draw_planar(G, with_labels=True, node_color=node_colors, node_size=10, cmap=plt.cm.rainbow)
    plt.savefig("out.png")

csp = dwavebinarycsp.ConstraintSatisfactionProblem(dwavebinarycsp.BINARY)
for state in vertices:
    variables = [state+"_"+str(i) for i in range(colors)]
    csp.add_constraint(one_hot_encoding, variables)

for neighbor in edges:
    v,u = neighbor
    for i in range(colors):
        variables = [v+"_"+str(i), u+"_"+str(i)]
        csp.add_constraint(not_same_color, variables)

bqm = dwavebinarycsp.stitch(csp)

    
sampler = DWaveSampler(solver={'topology__type': 'pegasus'})
embedding = EmbeddingComposite(sampler)
sampleset = embedding.sample(bqm, num_reads=1000)
backup("US Map Pegasus",sampleset)

for sample in sampleset: 
    if csp.check(sample): # works with the simulator...
        print("OK!")
        plot_map(sample)
        break
    print("Bad sample!")
