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

    def generate(self):
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
