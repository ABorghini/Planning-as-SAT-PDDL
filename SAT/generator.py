from pysat.solvers import Solver
import re
import time


class Generator:
    def __init__(self, config_file):
        # initial state file
        self.__initial_state_file = "initial_state.txt"

        c = {}
        # read config file
        with open(config_file, "r") as config:
            for line in config:
                l = line.strip().split(" ")
                c[l[0]] = []
                for i in range(1, len(l)):
                    if l[i] != "":
                        c[l[0]].append(l[i])

        # take data from config file
        self.__mosse = int(c["mosse"][0].strip())
        if self.__mosse < 0:
            print("Il numero di mosse deve essere un intero positivo")
            return

        dim = c["dimensione"][0].strip().split("x")
        if len(dim) < 2:
            print("Dimensione della griglia in formato errato")
            return

        self.__dim_x = int(dim[0])
        self.__dim_y = int(dim[1])

        p_robot = (
            c["posizione_iniziale_robot"][0]
            .replace("(", "")
            .replace(")", "")
            .strip()
            .split(",")
        )
        self.__robot_x = int(p_robot[0])
        self.__robot_y = int(p_robot[1])

        self.__p_piante = []
        for elem in c["posizione_piante"]:
            self.__p_piante.append(
                elem.replace("(", "").replace(")", "").strip().split(",")
            )

        self.__p_infestanti = []
        for elem in c["posizione_piante_infestanti"]:
            self.__p_infestanti.append(
                elem.replace("(", "").replace(")", "").strip().split(",")
            )

        self.__celle = []
        for i in range(self.__dim_x):
            for j in range(self.__dim_y):
                self.__celle.append([i, j])

    def solve(self):
        start = time.clock_gettime(time.CLOCK_MONOTONIC)
        # generate intial state
        self.initial_state_generator()

        # generate actions based on initial state
        self.__azioni = self.actions_generator()

        # generate constraints based on initial state
        self.constraints_generator()

        # generate final state
        self.final_state_generator()

        # generate actions and constrints for each time (from 0 to self.__mosse)
        self.moves_generator()

        # convert the problem in DIMACS CNF format
        self.convert_to_dimacs()

        # solve the problem
        with open("problem_dimacs.txt", "r") as f:
            l = []
            for line in f:
                line = [int(x) for x in line.strip().split(" ")]
                l.append(line)

        s = Solver(use_timer=True)
        for elem in l:
            s.add_clause(elem)

        solution = s.solve()
        end = time.clock_gettime(time.CLOCK_MONOTONIC)
        print(end - start)
        t = s.time()
        print(t)
        sat = "SATISFIABLE" if solution else "UNSATISFIABLE"
        print("The problem is: " + sat)

        if solution:
            self.__model_dimacs = s.get_model()
            self.__model = self.convert_from_dimacs()
            return solution, self.__model
        else:
            return solution, []

    def print_problem(self):
        modello_by_steps = {}
        infestante = []

        for l in self.__model:
            r = re.findall("_[0-9]+", l)
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
                    or re.findall("^move_to", elem)
                ):
                    mosse[str(i)] = elem

        for i in range(len(robot)):
            print("Passo " + str(i))
            self.print_step(
                robot[str(i)],
                piante[str(i)],
                innaffiate[str(i)],
                infestante,
                mosse[str(i)],
            )
        return

    def print_step(self, robot, piante, innaffiate, infestanti, mosse):
        robot_x = int(robot[0])
        robot_y = int(robot[1])
        dim_x = self.__dim_x
        dim_y = self.__dim_y
        problema = ""

        print(mosse + "\n" if mosse != [] else "-\n")
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

    def initial_state_generator(self):
        i_s = str(self.__mosse) + "\n\n"

        for i in range(self.__dim_x):
            for j in range(self.__dim_y):
                if i == self.__robot_x and j == self.__robot_y:
                    i_s += "r_0,(" + str(i) + "," + str(j) + ")\n"
                else:
                    i_s += "-r_0,(" + str(i) + "," + str(j) + ")\n"
        i_s += "\n"

        for i in range(self.__dim_x):
            for j in range(self.__dim_y):
                if [str(i), str(j)] in self.__p_piante:
                    i_s += "p_0,(" + str(i) + "," + str(j) + ")\n"
                else:
                    i_s += "-p_0,(" + str(i) + "," + str(j) + ")\n"
        i_s += "\n"

        for i in range(self.__dim_x):
            for j in range(self.__dim_y):
                if [str(i), str(j)] in self.__p_infestanti:
                    i_s += "infestante_(" + str(i) + "," + str(j) + ")\n"
                else:
                    i_s += "-infestante_(" + str(i) + "," + str(j) + ")\n"
        i_s += "\n"

        for i in range(self.__dim_x):
            for j in range(self.__dim_y):
                if [str(i), str(j)] not in self.__p_infestanti and [
                    str(i),
                    str(j),
                ] in self.__p_piante:
                    i_s += "-innaffiata_0,(" + str(i) + "," + str(j) + ")\n"

        with open(self.__initial_state_file, "w") as f:
            f.write(i_s)

    def adjacencies(self, cella_x, cella_y, x, y):
        adiacenze = []

        for i in range(-1, 2):
            if i != 0 and cella_x + i >= 0 and cella_x + i < x:
                adiacenze.append([cella_x + i, cella_y])
        for j in range(-1, 2):
            if j != 0 and cella_y + j >= 0 and cella_y + j < y:
                adiacenze.append([cella_x, cella_y + j])

        return adiacenze

    def move_to_generator(self):
        move_to = ""
        move = []

        for cella in self.__celle:
            cella_x = cella[0]
            cella_y = cella[1]
            adj = self.adjacencies(cella_x, cella_y, self.__dim_x, self.__dim_y)

            move.append("move_to_0,(" + str(cella_x) + "," + str(cella_y) + ")")
            move_to += "-move_to_0,(" + str(cella_x) + "," + str(cella_y) + ") "
            for c in adj:
                move_to += "r_0,(" + str(c[0]) + "," + str(c[1]) + ") "
            move_to += (
                "\n-move_to_0,("
                + str(cella_x)
                + ","
                + str(cella_y)
                + ") r_1,("
                + str(cella_x)
                + ","
                + str(cella_y)
                + ")\n"
            )

        with open("actions_and_constraints.txt", "w") as f:
            f.write(move_to + "\n")

        return move

    def estirpa_innaffia(self):
        actions = ""
        azioni = []
        for p in self.__p_piante:
            p_x = p[0]
            p_y = p[1]

            azioni.append("estirpa_0,(" + p_x + "," + p_y + ")")
            azioni.append("innaffia_0,(" + p_x + "," + p_y + ")")
            estirpa = "-estirpa_0,(" + p_x + "," + p_y + ") "
            actions += estirpa
            actions += "r_0,(" + p_x + "," + p_y + ")\n"
            actions += estirpa
            actions += "p_0,(" + p_x + "," + p_y + ")\n"
            actions += estirpa
            actions += "infestante_(" + p_x + "," + p_y + ")\n"
            actions += estirpa
            actions += "-p_1,(" + p_x + "," + p_y + ")\n"
            actions += estirpa
            actions += "r_1,(" + p_x + "," + p_y + ")\n\n"

            innaffia = "-innaffia_0,(" + p_x + "," + p_y + ") "
            actions += innaffia
            actions += "r_0,(" + p_x + "," + p_y + ")\n"
            actions += innaffia
            actions += "p_0,(" + p_x + "," + p_y + ")\n"
            actions += innaffia
            actions += "-infestante_(" + p_x + "," + p_y + ")\n"
            actions += innaffia
            actions += "-innaffiata_0,(" + p_x + "," + p_y + ")\n"
            actions += innaffia
            actions += "innaffiata_1,(" + p_x + "," + p_y + ")\n"
            actions += innaffia
            actions += "r_1,(" + p_x + "," + p_y + ")\n\n"

        with open("actions_and_constraints.txt", "a") as f:
            f.write(actions)

        return azioni

    def actions_generator(self):
        azioni = self.move_to_generator()
        azioni.extend(self.estirpa_innaffia())
        return azioni

    def one_action_x_time(self):
        s = ""
        for i in range(len(self.__azioni)):
            j = i + 1
            while j < len(self.__azioni):
                s += "-" + self.__azioni[i] + " -" + self.__azioni[j] + "\n"
                j += 1

        with open("actions_and_constraints.txt", "a") as f:
            f.write(s + "\n")

        return

    def at_least_one_action(self):
        s = ""
        for a in self.__azioni:
            s += a + " "

        with open("actions_and_constraints.txt", "a") as f:
            f.write(s + "\n\n")

        return

    def one_position_robot_x_time(self, posizioni):
        s = ""
        for i in range(len(posizioni)):
            j = i + 1
            while j < len(posizioni):
                s += "-" + posizioni[i] + " -" + posizioni[j] + "\n"
                j += 1

        with open("actions_and_constraints.txt", "a") as f:
            f.write(s + "\n")

        return

    def at_least_one_position_robot(self):
        s = ""
        pos = []
        for c in self.__celle:
            s += "r_1,(" + str(c[0]) + "," + str(c[1]) + ") "
            pos.append("r_1,(" + str(c[0]) + "," + str(c[1]) + ")")

        with open("actions_and_constraints.txt", "a") as f:
            f.write(s + "\n\n")

        return pos

    def robot_position_constraint(self, posizioni):
        s = ""
        for elem in posizioni:
            s += "-" + elem + " "
            for a in self.__azioni:
                if elem[-5:] in a:
                    s += a + " "
            s += "\n"

        with open("actions_and_constraints.txt", "a") as f:
            f.write(s + "\n")

        return

    def plant_position_constraint(self):
        s = ""
        for a in self.__azioni:
            if "estirpa" in a:
                s += "p_1," + a[-5:] + " "
                s += "-p_0," + a[-5:] + " "
                s += a + "\n"

        with open("actions_and_constraints.txt", "a") as f:
            f.write(s + "\n")

        return

    def innaffiata_constraint(self):
        s = ""
        for a in self.__azioni:
            if "innaffia" in a:
                s += "-innaffiata_1," + a[-5:] + " "
                s += a + " "
                s += "innaffiata_0," + a[-5:] + "\n"

        with open("actions_and_constraints.txt", "a") as f:
            f.write(s + "\n")

        return

    def constraints_generator(self):
        self.one_action_x_time()
        self.at_least_one_action()
        posizioni = self.at_least_one_position_robot()
        self.one_position_robot_x_time(posizioni)

        self.robot_position_constraint(posizioni)
        self.plant_position_constraint()
        self.innaffiata_constraint()

    def final_state_generator(self):
        final_state = ""
        for pos in self.__p_piante:
            if pos in self.__p_infestanti:
                final_state += (
                    "-p_" + str(self.__mosse + 1) + ",(" + pos[0] + "," + pos[1] + ")\n"
                )
            else:
                final_state += (
                    "innaffiata_"
                    + str(self.__mosse + 1)
                    + ",("
                    + pos[0]
                    + ","
                    + pos[1]
                    + ")\n"
                )

        with open("final_state.txt", "w") as f:
            f.write(final_state)

        return

    def moves_generator(self):
        move = {}

        with open("actions_and_constraints.txt", "r") as f:
            move[0] = ""
            for line in f:
                if line != "\n":
                    move[0] += line

        for i in range(self.__mosse):
            move[i + 1] = move[0].replace("move_to_0", "move_to_" + str(i + 1))
            move[i + 1] = move[i + 1].replace("estirpa_0", "estirpa_" + str(i + 1))
            move[i + 1] = move[i + 1].replace(
                "innaffiata_1", "innaffiata_" + str(i + 2)
            )
            move[i + 1] = move[i + 1].replace(
                "innaffiata_0", "innaffiata_" + str(i + 1)
            )
            move[i + 1] = move[i + 1].replace("innaffia_0", "innaffia_" + str(i + 1))
            move[i + 1] = move[i + 1].replace("p_1", "p_" + str(i + 2))
            move[i + 1] = move[i + 1].replace("p_0", "p_" + str(i + 1))
            move[i + 1] = move[i + 1].replace("r_1", "r_" + str(i + 2))
            move[i + 1] = move[i + 1].replace("r_0", "r_" + str(i + 1))

        with open("moves.txt", "w") as f:
            for k in move:
                f.write(move[k] + "\n")

    def return_moves(self):
        return self.__mosse

    def create_dictionary(self, f):
        d = {}
        l = re.findall("[0-9]+", f)
        i = 1

        for elem in l:
            if elem not in d.values():
                d[i] = elem
                i += 1

        return d

    def convert_to_dimacs(self):
        file = ""
        literals = []
        with open("problem.txt", "r") as f:
            for line in f:
                if line != "\n":
                    file += line
                    literals.extend(
                        re.findall(
                            "[a-z]+_\([0-9]+,[0-9]+\)|[a-z]*_?[a-z]+_[0-9]+,\([0-9]+,[0-9]+\)",
                            line,
                        )
                    )

        dimacs_dict = {}

        i = 1
        # create
        for l in literals:
            if l not in dimacs_dict.values():
                dimacs_dict[str(i)] = l
                i += 1

        self.__dimacs_dict = dimacs_dict
        # self.__to_dimacs_dict = {lit: i for i, lit in self.__from_dimacs_dict.items()}

        for literal in dimacs_dict:
            file = file.replace(dimacs_dict[literal], literal)

        with open("problem_dimacs.txt", "w") as f:
            f.write(file)

    def convert_from_dimacs(self):
        model = []
        dimacs_dict = self.__dimacs_dict
        model_dimacs = self.__model_dimacs

        for elem in model_dimacs:
            e = str(elem)
            if e[0] == "-":
                model.append(e.replace(e[1:], dimacs_dict[e[1:]]))
            else:
                model.append(e.replace(e, dimacs_dict[e]))

        return model
