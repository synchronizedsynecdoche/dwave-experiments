# https://docs.ocean.dwavesys.com/en/latest/examples/hybrid1.html#hybrid1

import dimod
import networkx as nx
import random
graph = nx.barabasi_albert_graph(100,3,seed=1)
h = {v: 0.0 for v in graph.nodes}
J = {edge: random.choice([-1,1]) for edge in graph.edges}
bqm = dimod.BQM(h,J,offset=0,vartype=dimod.SPIN)

import hybrid
hybrid.logger.setLevel(hybrid.logging.DEBUG) 

workflow = hybrid.Loop(
    hybrid.RacingBranches(
        hybrid.InterruptableTabuSampler(max_time=0),
        hybrid.EnergyImpactDecomposer(size=100, rolling=True, rolling_history=0.75) | hybrid.QPUSubproblemAutoEmbeddingSampler(num_reads=1)| hybrid.SplatComposer()
    )| hybrid.ArgMin() ,
    convergence=3 
)

result = hybrid.HybridSampler(workflow).sample(bqm)
hybrid.Unwind(workflow)
print("Solution: sample={}".format(result.first))
hybrid.print_structure(workflow)
print("-----------------------")
hybrid.print_counters(workflow)