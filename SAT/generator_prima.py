import sys

initial_state_file = "initial_state.txt"


def adjacencies(cella_x, cella_y, x, y):
    adiacenze = []

    for i in range(-1, 2):
        if i != 0 and cella_x + i >= 0 and cella_x + i < x:
            adiacenze.append([cella_x + i, cella_y])
    for j in range(-1, 2):
        if j != 0 and cella_y + j >= 0 and cella_y + j < y:
            adiacenze.append([cella_x, cella_y + j])

    return adiacenze


def move_to_generator(celle, x, y):
    move_to = ""
    move = []

    for cella in celle:
        cella_x = cella[0]
        cella_y = cella[1]
        adj = adjacencies(cella_x, cella_y, x, y)

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


def estirpa_innaffia(celle, piante):
    actions = ""
    azioni = []
    for p in piante:
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


def actions_generator(celle, dim_x, dim_y, piante):
    azioni = move_to_generator(celle, dim_x, dim_y)
    azioni.extend(estirpa_innaffia(celle, piante))
    return azioni


def one_action_x_time(azioni):
    s = ""
    for i in range(len(azioni)):
        j = i + 1
        while j < len(azioni):
            s += "-" + azioni[i] + " -" + azioni[j] + "\n"
            j += 1

    with open("actions_and_constraints.txt", "a") as f:
        f.write(s + "\n")

    return


def at_least_one_action(azioni):
    s = ""
    for a in azioni:
        s += a + " "

    with open("actions_and_constraints.txt", "a") as f:
        f.write(s + "\n\n")

    return


def one_position_robot_x_time(posizioni):
    s = ""
    for i in range(len(posizioni)):
        j = i + 1
        while j < len(posizioni):
            s += "-" + posizioni[i] + " -" + posizioni[j] + "\n"
            j += 1

    with open("actions_and_constraints.txt", "a") as f:
        f.write(s + "\n")

    return


def at_least_one_position_robot(celle):
    s = ""
    pos = []
    for c in celle:
        s += "r_1,(" + str(c[0]) + "," + str(c[1]) + ") "
        pos.append("r_1,(" + str(c[0]) + "," + str(c[1]) + ")")

    with open("actions_and_constraints.txt", "a") as f:
        f.write(s + "\n\n")

    return pos


def robot_position_constraint(posizioni, azioni):
    s = ""
    for elem in posizioni:
        s += "-" + elem + " "
        for a in azioni:
            if elem[-5:] in a:
                s += a + " "
        s += "\n"

    print(s)

    with open("actions_and_constraints.txt", "a") as f:
        f.write(s + "\n")

    return


def plant_position_constraint(azioni):
    s = ""
    for a in azioni:
        if "estirpa" in a:
            s += "p_1," + a[-5:] + " "
            s += "-p_0," + a[-5:] + " "
            s += a + "\n"
    print(s)

    with open("actions_and_constraints.txt", "a") as f:
        f.write(s + "\n")

    return


def innaffiata_constraint(azioni):
    s = ""
    for a in azioni:
        if "innaffia" in a:
            s += "-innaffiata_1," + a[-5:] + " "
            s += a + " "
            s += "innaffiata_0," + a[-5:] + "\n"

    print(s)

    with open("actions_and_constraints.txt", "a") as f:
        f.write(s + "\n")

    return


def constraints_generator(initial_state, azioni, celle):
    one_action_x_time(azioni)
    at_least_one_action(azioni)
    posizioni = at_least_one_position_robot(celle)
    one_position_robot_x_time(posizioni)

    robot_position_constraint(posizioni, azioni)
    plant_position_constraint(azioni)
    innaffiata_constraint(azioni)


def initial_state_generator(mosse, dim_x, dim_y, robot_x, robot_y, piante, infestanti):
    i_s = str(mosse) + "\n\n"

    for i in range(dim_x):
        for j in range(dim_y):
            if i == robot_x and j == robot_y:
                i_s += "r_0,(" + str(i) + "," + str(j) + ")\n"
            else:
                i_s += "-r_0,(" + str(i) + "," + str(j) + ")\n"
    i_s += "\n"

    for i in range(dim_x):
        for j in range(dim_y):
            if [str(i), str(j)] in piante:
                i_s += "p_0,(" + str(i) + "," + str(j) + ")\n"
            else:
                i_s += "-p_0,(" + str(i) + "," + str(j) + ")\n"
    i_s += "\n"

    for i in range(dim_x):
        for j in range(dim_y):
            if [str(i), str(j)] in infestanti:
                i_s += "infestante_(" + str(i) + "," + str(j) + ")\n"
            else:
                i_s += "-infestante_(" + str(i) + "," + str(j) + ")\n"
    i_s += "\n"

    for i in range(dim_x):
        for j in range(dim_y):
            if [str(i), str(j)] not in infestanti and [str(i), str(j)] in piante:
                i_s += "-innaffiata_0,(" + str(i) + "," + str(j) + ")\n"

    with open(initial_state_file, "w") as f:
        f.write(i_s)


if __name__ == "__main__":
    c = {}
    with open("problem.config", "r") as config:
        for line in config:
            l = line.strip().split(" ")
            c[l[0]] = []
            for i in range(1, len(l)):
                if l[i] != "":
                    c[l[0]].append(l[i])

    # print(c)

    mosse = int(c["mosse"][0].strip())
    if mosse < 0:
        print("Il numero di mosse deve essere un intero positivo")
        sys.exit(0)

    dim = c["dimensione"][0].strip().split("x")
    if len(dim) < 2:
        print("Dimensione della griglia in formato errato")
        sys.exit(0)

    dim_x = int(dim[0])
    dim_y = int(dim[1])

    p_robot = (
        c["posizione_iniziale_robot"][0]
        .replace("(", "")
        .replace(")", "")
        .strip()
        .split(",")
    )
    robot_x = int(p_robot[0])
    robot_y = int(p_robot[1])

    p_piante = []
    for elem in c["posizione_piante"]:
        p_piante.append(elem.replace("(", "").replace(")", "").strip().split(","))

    p_infestanti = []
    for elem in c["posizione_piante_infestanti"]:
        p_infestanti.append(elem.replace("(", "").replace(")", "").strip().split(","))

    print_problem(dim, p_robot, p_piante, p_infestanti)

    initial_state_generator(
        mosse, dim_x, dim_y, robot_x, robot_y, p_piante, p_infestanti
    )

    celle = []
    for i in range(dim_x):
        for j in range(dim_y):
            celle.append([i, j])

    azioni = actions_generator(celle, dim_x, dim_y, p_piante)

    constraints_generator(initial_state_file, azioni, celle)
