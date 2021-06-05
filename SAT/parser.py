with open("SAT_solver/2x2.cnf", "r") as f:
    l = []
    for line in f:
        line= [int(x) for x in line.strip().split(" ")]
        l.append(line)

print(l)
            