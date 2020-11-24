# https://docs.ocean.dwavesys.com/en/latest/examples/hybrid1.html#hybrid1

import dimod
import networkx as nx
import random
from pyqubo import Spin
import numpy as np
arr =  [1]*100 + [-1]*100
print(arr)
H = 0

for i in range(len(arr)):
    if(i % 10 == 0): #high impact variables
        H += 1000*arr[i]*Spin(f'x_{i}')
        continue
    H += arr[i]*Spin(f'x_{i}')

H *= H
print("Compiling...")
model = H.compile()
bqm = model.to_bqm()
print("OK")

import hybrid
hybrid.logger.setLevel(hybrid.logging.DEBUG) 

workflow = hybrid.Loop(
    hybrid.RacingBranches(
        hybrid.InterruptableSimulatedAnnealingProblemSampler(),
        hybrid.EnergyImpactDecomposer(size=10, rolling=True, rolling_history=.3) | hybrid.QPUSubproblemAutoEmbeddingSampler(num_reads=2)| hybrid.SplatComposer()
    )| hybrid.ArgMin() ,
    convergence=3 
)

# not our workflow
result = hybrid.KerberosSampler().sample(bqm)
hybrid.Unwind(workflow)
print("Solution: sample={}".format(result.first))
#hybrid.print_structure(workflow)
print("-----------------------")
#hybrid.print_counters(workflow)