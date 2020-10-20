#https://docs.ocean.dwavesys.com/en/stable/examples/multi_gate.html
import dwavebinarycsp
 
def strange(a,b):
    return a or not b

csp = dwavebinarycsp.ConstraintSatisfactionProblem(dwavebinarycsp.BINARY)

csp.add_constraint(strange, ['a','b'])
bqm = dwavebinarycsp.stitch(csp)

from dwave.system import DWaveSampler, EmbeddingComposite
sampler = EmbeddingComposite(DWaveSampler())

dataset = sampler.sample(bqm, num_reads=10)

print(dataset)