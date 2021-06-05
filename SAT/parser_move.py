def gen_mosse(n):
    move = {}

    with open("move.txt", "r") as f:
        move[0] = ""
        for line in f:
            if line!="\n":
                move[0] += line


    for i in range(n):
        move[i+1] = move[0].replace("move_to_0", "move_to_"+str(i+1))
        move[i+1] = move[i+1].replace("estirpa_0", "estirpa_"+str(i+1))
        move[i+1] = move[i+1].replace("innaffiata_1", "innaffiata_"+str(i+2))
        move[i+1] = move[i+1].replace("innaffiata_0", "innaffiata_"+str(i+1))
        move[i+1] = move[i+1].replace("innaffia_0", "innaffia_"+str(i+1))
        move[i+1] = move[i+1].replace("p_1", "p_"+str(i+2))
        move[i+1] = move[i+1].replace("p_0", "p_"+str(i+1))
        move[i+1] = move[i+1].replace("r_1", "r_"+str(i+2))
        move[i+1] = move[i+1].replace("r_0", "r_"+str(i+1))
        

    with open("problema_tot.txt", "w") as f:
        for k in move:
            f.write(move[k])
        

