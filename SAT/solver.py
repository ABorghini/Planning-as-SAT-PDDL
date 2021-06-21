from pysat.solvers import *
import numpy as np
import re


def print_step(dim, robot, piante, innaffiate, infestanti, mosse):
    robot_x = int(robot[0])
    robot_y = int(robot[1])
    dim_x = int(dim[0])
    dim_y = int(dim[1])
    problema = ""

    print(mosse)
    for i in range(dim_x):
        for j in range(dim_y):
            in_cella = ""
            if i == robot_x and j == robot_y:
                in_cella += "R"
            if [i, j] in piante:
                if [i, j] in infestanti:
                    if in_cella != "":
                        in_cella += "+I"
                    else:
                        in_cella += "I"
                else:
                    if [i, j] in innaffiate:
                        if in_cella != "":
                            in_cella += "+S'"
                        else:
                            in_cella += "S'"
                    else:
                        if in_cella != "":
                            in_cella += "+S"
                        else:
                            in_cella += "S"
            if in_cella == "":
                in_cella += "-"
            problema += in_cella + " "
        problema += "\n"

    print(problema)


def print_problem(modello_list):
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
        if re.findall("^infestante_\([0-9]+,[0-9]+\)", l):

            e = re.findall("[0-9]+,[0-9]+", l)[0].strip().split(",")
            infestante.append([int(e[0]), int(e[1])])

    robot = {}
    piante = {}
    innaffiate = {}
    mosse = {}

    for i in range(len(modello_by_steps)):
        piante[str(i)] = []
        robot[str(i)] = []
        innaffiate[str(i)] = []
        mosse[str(i)] = []
        for elem in modello_by_steps[str(i)]:
            if re.findall("^r_([0-9]+),\([0-9]+,[0-9]+\)", elem):
                e = re.findall("[0-9]+,[0-9]+", elem)[0].strip().split(",")
                robot[str(i)] = [int(e[0]), int(e[1])]
            if re.findall("^p_([0-9]+),\([0-9]+,[0-9]+\)", elem):
                e = re.findall("[0-9]+,[0-9]+", elem)[0].strip().split(",")
                piante[str(i)].append([int(e[0]), int(e[1])])
            if re.findall("^innaffiata_([0-9]+),\([0-9]+,[0-9]+\)", elem):
                e = re.findall("[0-9]+,[0-9]+", elem)[0].strip().split(",")
                innaffiate[str(i)].append([int(e[0]), int(e[1])])
            if (
                re.findall("^innaffia_", elem)
                or re.findall("^estirpa", elem)
                or re.findall("^moveto", elem)
            ):
                mosse[str(i)] = elem

    for i in range(len(robot)):
        print("Passo " + str(i) + "\n")
        print_step(
            [3, 3],
            robot[str(i)],
            piante[str(i)],
            innaffiate[str(i)],
            infestante,
            mosse[str(i)],
        )
    return


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

            print_problem(modello_list)

        else:
            report.write("MODEL: -\n")
        s.delete()
        print("Generated report file")
