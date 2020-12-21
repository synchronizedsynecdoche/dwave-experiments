# Ising formulations of many NP problems 2.1
from dwave.system import DWaveSampler, EmbeddingComposite, SimulatedAnnealer
from pyqubo import Spin
import pickle
from datetime import datetime
import numpy as np


def backup(expName, topo, samples):

    with open("data/"+expName + topo + str(datetime.now()), "wb") as f:
                
            pickle.dump(samples, f)
arr = [4,4,8,4,4,8]
#np.random.randint(1,high=100,size=20)
print(arr)
H = 0

for i in range(len(arr)):
    H += arr[i]*Spin(f'x_{i}')

H *= H
model = H.compile()
sampler = DWaveSampler()
embedded = EmbeddingComposite(sampler)
bqm = model.to_bqm() # we need pyqubo>=1.0.0

print("embedding and sampling...")
sampleset = embedded.sample(bqm, num_reads=100)
backup("num partitioning arr", "Chimera", arr)
backup("num partitioning", "Chimera", sampleset)
decoded_samples = model.decode_sampleset(sampleset)
best = min(decoded_samples, key=lambda x:x.energy)
# decision version of the partitioning problemm: does there exist a partition?
print(best)
# how close are we?
print(best.energy)