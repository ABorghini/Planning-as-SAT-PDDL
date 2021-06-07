from pysat.solvers import *
import numpy as np

def solve():
    with open("report.txt", "w") as report:
        with open("problem_dimacs.txt", "r") as f:
            l = []
            flattened_list = []
            for line in f:
                line= [int(x) for x in line.strip().split(" ")]
                l.append(line)
                flattened_list.extend(line)

        s = Solver(use_timer=True)
        for elem in l:
            s.add_clause(elem)

        ris = s.solve()
        t = s.time()

        sat = "SAT" if ris else "UNSAT"
        report.write("RESULT: "+sat+"\n")
        report.write("EXEC-TIME: "+str(t)+"\n")
        print(sat)

        if ris:
            model = s.get_model()
            modello_txt = ""

            replace_words = {"1":"infestante", "2": "innaffiata", "3": "moveto", "4": "estirpa", "5": "innaffia", "6": "p", "7": "r"}
            for elem in model:
                if elem in flattened_list:
                    lit = str(elem)
                    literal = ""
                    if lit[0]!= "-":
                        literal = replace_words[lit[0]]       
                        literal += "_" + lit[1:-2] + ",(" + lit[-2:-1] + "," + lit[-1:] + ")"
                    else:
                        literal = "-"+replace_words[lit[1]]   
                        literal += "_" + lit[2:-2] + ",(" + lit[-2:-1] + "," + lit[-1:] + ")"
                    modello_txt += literal+"\n"
            
            report.write("MODEL:\n"+modello_txt)
              
        else:
            report.write("MODEL: -\n")
        s.delete()
        print("Generated report file") 
