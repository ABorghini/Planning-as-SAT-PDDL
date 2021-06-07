def generate_final_state():
    with open("initial_state.txt", "r") as f:
        p = []
        inf = []
        num_mosse = int(f.readline().strip())
        for line in f:
            line = line.strip()
            if len(line)>1:
                if line[0]=="p":
                    p.append(line)
                elif "infestante" in line:
                    inf.append(line)

    final_state = ""
    coord = ""
    for pos in p:
        coord = pos[-5:]
        for i in inf:
            if i[-5:]==coord:
                if i[0]=="-": 
                    final_state += "innaffiata_"+str(num_mosse+1)+","+coord+"\n"
                else: 
                    final_state += "-p_"+str(num_mosse+1)+","+coord+"\n"

    """ with open("final_state.txt", "w") as f:
        f.write(final_state) """
    return num_mosse