def problem_gen():
    i_s = ""
    with open("initial_state.txt", "r") as f:
        f.readline()
        for line in f:
            i_s += line          

    a = ""
    with open("moves.txt", "r") as f:
        for line in f:
            a += line 

    f_s = ""
    with open("final_state.txt", "r") as f:
        for line in f:
            f_s += line 
        
    with open("problem.txt", "w") as f:
        f.write(i_s+"\n")
        f.write(a+"\n")
        f.write(f_s)
    