from pysat.solvers import *
import numpy as np
import re
from generator import print_problem


def solve():
    with open("report.txt", "w") as report:
        with open("problem_dimacs.txt", "r") as f:
            l = []
            flattened_list = []
            for line in f:
                line = [int(x) for x in line.strip().split(" ")]
                l.append(line)
                flattened_list.extend(line)

        s = Solver(use_timer=True)
        for elem in l:
            s.add_clause(elem)

        ris = s.solve()
        t = s.time()

        sat = "SAT" if ris else "UNSAT"
        report.write("RESULT: " + sat + "\n")
        report.write("EXEC-TIME: " + str(t) + "\n")
        print(sat)

        if ris:
            model = s.get_model()
            modello_txt = ""
            modello_list = []

            replace_words = {
                "1": "infestante",
                "2": "innaffiata",
                "3": "moveto",
                "4": "estirpa",
                "5": "innaffia",
                "6": "p",
                "7": "r",
            }

            for elem in model:
                if elem in flattened_list:
                    lit = str(elem)
                    literal = ""
                    if lit[0] != "-":
                        literal = replace_words[lit[0]]
                        if lit[1:-2] == "":
                            literal += "_(" + lit[-2:-1] + "," + lit[-1:] + ")"
                        else:
                            literal += (
                                "_"
                                + lit[1:-2]
                                + ",("
                                + lit[-2:-1]
                                + ","
                                + lit[-1:]
                                + ")"
                            )
                    else:
                        literal = "-" + replace_words[lit[1]]
                        if lit[2:-2] == "":
                            literal += "_(" + lit[-2:-1] + "," + lit[-1:] + ")"
                        else:
                            literal += (
                                "_"
                                + lit[2:-2]
                                + ",("
                                + lit[-2:-1]
                                + ","
                                + lit[-1:]
                                + ")"
                            )
                    modello_txt += literal + "\n"
                    modello_list.append(literal)

            # report.write("MODEL:\n" + modello_txt)

            modello_by_steps = {}
            infestante = []
            pattern = "_[0-9]+"

            for l in modello_list:
                r = re.findall(pattern, l)
                if r:
                    idx = r[0][1:]
                    if idx not in modello_by_steps:
                        modello_by_steps[idx] = []
                    modello_by_steps[idx].append(l)
                if "infestante" in l:
                    infestante.append(l)

            # print(modello_by_steps)
            print(infestante)
            robot = {}
            piante = {}

            for i in range(len(modello_by_steps)):
                piante[str(i)] = []
                for elem in modello_by_steps[str(i)]:
                    if re.findall("^r_([0-9]+),\([0-9]+,[0-9]+\)", elem):
                        e = re.findall("[0-9]+,[0-9]+", elem)[0].strip().split(",")
                        robot[str(i)] = [int(e[0]), int(e[1])]
                    if re.findall("^p_([0-9]+),\([0-9]+,[0-9]+\)", elem):
                        e = re.findall("[0-9]+,[0-9]+", elem)[0].strip().split(",")
                        piante[str(i)].append([int(e[0]), int(e[1])])
            print(robot)
            print(piante)

            for i in range(len(robot)):
                print_problem([3, 3], robot[str(i)], piante[str(i)], infestante)

        else:
            report.write("MODEL: -\n")
        s.delete()
        print("Generated report file")
