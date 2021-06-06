azioni = ["move_to_0,(0,0)",
"move_to_0,(1,0)", 
"move_to_0,(2,0)",
"move_to_0,(0,1)",
"move_to_0,(1,1)",
"move_to_0,(2,1)",
"move_to_0,(0,2)",
"move_to_0,(1,2)",
"move_to_0,(2,2)",
"estirpa_0,(0,0)",
"estirpa_0,(0,1)",
"estirpa_0,(0,2)",
"estirpa_0,(1,0)",
"estirpa_0,(1,1)",
"estirpa_0,(1,2)",
"estirpa_0,(2,0)",
"estirpa_0,(2,1)",
"estirpa_0,(2,2)",
"innaffia_0,(0,0)",
"innaffia_0,(0,1)",
"innaffia_0,(0,2)",
"innaffia_0,(1,0)",
"innaffia_0,(1,1)",
"innaffia_0,(1,2)",
"innaffia_0,(2,0)",
"innaffia_0,(2,1)",
"innaffia_0,(2,2)"]

combinazioni = ""
for i in range(len(azioni)):
    j=i+1
    while j<len(azioni):
        combinazioni += "-"+azioni[i] +" -"+azioni[j] +"\n"
        j += 1

estirpa = ""
e = ""
for i in range(3):
    for j in range(3):
        e = "-estirpa_0,("+str(i)+","+str(j)+") " 
        estirpa += e + "r_0,("+str(i)+","+str(j)+")\n"
        estirpa += e + "p_0,("+str(i)+","+str(j)+")\n"
        estirpa += e + "infestante_("+str(i)+","+str(j)+")\n"
        estirpa += e + "-p_1,("+str(i)+","+str(j)+")\n"
        estirpa += e + "r_1,("+str(i)+","+str(j)+")\n"


innaffia = ""
inn = ""
for i in range(3):
    for j in range(3):
        inn = "-innaffia_0,("+str(i)+","+str(j)+") " 
        innaffia += inn + "r_0,("+str(i)+","+str(j)+")\n"
        innaffia += inn + "p_0,("+str(i)+","+str(j)+")\n"
        innaffia += inn + "-infestante_("+str(i)+","+str(j)+")\n"
        innaffia += inn + "-innaffiata_0,("+str(i)+","+str(j)+")\n"
        innaffia += inn + "innaffiata_1,("+str(i)+","+str(j)+")\n"
        innaffia += inn + "r_1,("+str(i)+","+str(j)+")\n"


posizioni = []
p = ""
for i in range(3):
    for j in range(3):
        posizioni.append("r_1,("+str(i)+","+str(j)+")")

print(posizioni)
combi_posizioni = ""
for i in range(len(posizioni)):
    j=i+1
    while j<len(posizioni):
        combi_posizioni += "-"+posizioni[i] +" -"+posizioni[j] +"\n"
        j += 1

pos = ""
for i in range(3):
    for j in range(3):
        pos += "-r_1,("+str(i)+","+str(j)+") " 
        pos += "move_to_0,("+str(i)+","+str(j)+") "
        pos += "innaffia_0,("+str(i)+","+str(j)+") "
        pos += "estirpa_0,("+str(i)+","+str(j)+")\n"

for i in range(3):
    for j in range(3):
        pos += "p_1,("+str(i)+","+str(j)+") " 
        pos += "estirpa_0,("+str(i)+","+str(j)+") "
        pos += "-p_0,("+str(i)+","+str(j)+")\n"

for i in range(3):
    for j in range(3):
        pos += "-innaffiata_1,("+str(i)+","+str(j)+") " 
        pos += "innaffia_0,("+str(i)+","+str(j)+") "
        pos += "innaffiata_0,("+str(i)+","+str(j)+")\n"

pos = ""

for i in range(3):
    for j in range(3):
        pos += "move_to_0,("+str(i)+","+str(j)+") " 

for i in range(3):
    for j in range(3):
        pos += "estirpa_0,("+str(i)+","+str(j)+") " 

for i in range(3):
    for j in range(3):
        pos += "innaffia_1,("+str(i)+","+str(j)+") " 

print(pos+"\n")