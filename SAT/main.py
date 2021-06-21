from generator import Generator

if __name__ == "__main__":
    # generate all the clauses describing the problem
    generator = Generator("problem.config")
    generator.generate()
    mosse = generator.return_moves()

    # convert the clauses in DIMACS format
