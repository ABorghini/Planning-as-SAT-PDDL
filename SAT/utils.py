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
        with open("problem.txt", "r") as f:
            for line in f:
                if line != "\n":
                    file += line

        file = file.replace("(", "")
        file = file.replace(")", "")
        file = file.replace(",", "")
        file = file.replace("_", "")
        file = file.replace("infestante", "1")
        file = file.replace("innaffiata", "2")
        file = file.replace("moveto", "3")
        file = file.replace("estirpa", "4")
        file = file.replace("innaffia", "5")
        file = file.replace("p", "6")
        file = file.replace("r", "7")

        dict = self.create_dictionary(file)

        with open("problem_dimacs.txt", "w") as f:
            f.write(file)