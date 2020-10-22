# Ising formulations of many NP problems 2.1
from neal import SimulatedAnnealingSampler
from pyqubo import Spin

arr = [8,4,4,8,4,4]
H = 0

for i in range(len(arr)):
    H += arr[i]*Spin(f'x_{i}')

H *= H
model = H.compile()
sampler = SimulatedAnnealingSampler()
bqm = model.to_bqm() # we need pyqubo>=1.0.0

sampleset = sampler.sample(bqm, num_reads=100)
decoded_samples = model.decode_sampleset(sampleset)
best = min(decoded_samples, key=lambda x:x.energy)
print(best)