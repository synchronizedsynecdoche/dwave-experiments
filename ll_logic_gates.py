from dwave.system import DWaveSampler, EmbeddingComposite
from neal import  SimulatedAnnealingSampler
'''
lAND_qubo = {('x1', 'x2'): 1, ('x1', 'z'): -2, ('x2', 'z'): -2, ('z', 'z'): 3}
sampler = SimulatedAnnealingSampler()
sampleset = sampler.sample_qubo(lAND_qubo,num_reads=10)
print(sampleset)
'''

def guarded_num_reads(x):
    if x > 100:
        return 100
    return x

def generateSimulatedSamples(qubo, num_reads=100):

    #https://docs.ocean.dwavesys.com/projects/neal/en/latest/reference/generated/neal.sampler.SimulatedAnnealingSampler.sample.html
    return SimulatedAnnealingSampler().sample_qubo(qubo, num_reads=num_reads)

def generateRealSamples(qubo, num_reads=10):

    sampler = DWaveSampler()
    embedding = EmbeddingComposite(sampler)
    return embedding.sample_qubo(qubo, num_reads=guarded_num_reads(num_reads))


lNAND_qubo = {('x_1', 'x_2') : 1, ('z','z'): -1}
lNOR_qubo = {('x_1', 'x_1'): 2, ('x_2', 'x_2'):2, ('z', 'z'):-1}
# trying Ising models from http://eda.ee.ucla.edu/pub/C166.pdf
l2_qubo = {('x','x'): - 1, ('y','y'):-1, ('z','z'): 2,
           ('x','z'): -2, ('y', 'z'):-2, ('x','y'): 1}

sampleset = generateSimulatedSamples(l2_qubo, num_reads=100)
print(sampleset)