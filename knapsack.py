# Ising formulations of many NP problems 5.2
from neal import SimulatedAnnealingSampler
from pyqubo import Binary
from pprint import pprint
from datetime import datetime
import pickle
from dwave.system import DWaveSampler, EmbeddingComposite
from pprint import pprint
def backup(expName, topo, samples):

    with open("data/"+expName + topo + str(datetime.now()), "wb") as f:
                
            pickle.dump(samples, f)

# I am lazy and took these values from a CS 381 problem
vals = [1,6,18,22,28]
weights = [1,2,5,6,7]
W = 11

A = 100
# We need B*max(vals) < A so the H_B doesn't "overpower" H_A
B = 2*28 


# y_k is 1 if the final weight is k and 0 otherwise
final_weight_term = 0
for i in range(W):
    final_weight_term += Binary(f'y_{i}')
final_weight_term = A*(1 - final_weight_term)**2

# we want to weight of the objects to sum to the final weight:

ft = 0
st = 0
final_enforcement_term = 0

for i in range(len(vals)):
    st += weights[i]*Binary(f'x_{i}')
for i in range(W):
    ft += (i+1)*Binary(f'y_{i}') -st# need n to start from 1 not 0!

final_enforcement_term = A*(ft )**2
H_A = final_weight_term + final_enforcement_term

H_B = 0
for i in range(len(vals)):
    H_B += vals[i]*Binary(f'x_{i}')

H_B = -B*H_B

H = H_A + H_B

model = H.compile()

bqm = model.to_bqm()
sampler = DWaveSampler(solver={'topology__type': 'pegasus'})
embedded = EmbeddingComposite(sampler)
print("embedding and sampling...")
sampleset = embedded.sample(bqm, num_reads=10000)
backup("knapsack inside sum fixed", "Pegasus", sampleset)
best = min(model.decode_sampleset(sampleset), key=lambda x: x.energy)

print(best.energy)
print(best)


