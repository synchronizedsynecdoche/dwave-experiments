#Patrick
import ast 

# expects the last line of output
def resultToDict(filename, energy):
    f = open(filename)
    result = f.read()
    f.close()

    d = ast.literal_eval(result)

    report = []
    for k,v in zip(d.keys(), d.values()):
        report.append(str(v))

    returnable = [[energy, report]]
    return returnable

print(str(resultToDict("shortSim.txt", -19.653883129768836)).replace("\'", "\""))