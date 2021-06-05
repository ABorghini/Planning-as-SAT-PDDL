from pysat.solvers import Glucose3
import numpy as np

def solve():
    with open("problema_tot_dimacs.txt", "r") as f:
        l = []
        for line in f:
            line= [int(x) for x in line.strip().split(" ")]
            l.append(line)

    g = Glucose3()
    for elem in l:
        g.add_clause(elem)

    print(f"{g.solve()} -> SAT") if g.solve() else print(f"{g.solve()} -> UNSAT")

    if g.solve():
        flattened_list = []
        for clause in l:
            flattened_list.extend(clause)

        model = g.get_model()
        modello = []
        modello_txt = ""
        for elem in model:
            if elem in flattened_list:
                lit = str(elem)
                literal = ""
                if lit[0]!= "-":
                    if lit[0]=="1": literal = "infestante"          
                    elif lit[0] == "2": literal = "innaffiata"
                    elif lit[0] == "3": literal = "moveto"
                    elif lit[0] == "4": literal = "estirpa" 
                    elif lit[0] == "5": literal = "innaffia"
                    elif lit[0] == "6": literal = "p"
                    elif lit[0] == "7": literal = "r"
                    literal += "_" + lit[1:-2] + ",(" + lit[-2:-1] + "," + lit[-1:] + ")"
                else:
                    if lit[1]=="1": literal = "-infestante"          
                    elif lit[1] == "2": literal = "-innaffiata"
                    elif lit[1] == "3": literal = "-moveto"
                    elif lit[1] == "4": literal = "-estirpa" 
                    elif lit[1] == "5": literal = "-innaffia"
                    elif lit[1] == "6": literal = "-p"
                    elif lit[1] == "7": literal = "-r" 
                    literal += "_" + lit[2:-2] + ",(" + lit[-2:-1] + "," + lit[-1:] + ")"
                modello.append(literal)
                modello_txt += literal+"\n"
        
        with open("result.txt", "w") as f:
            f.write(modello_txt)
        
        mod = np.sort(modello)
        print(mod)


    
