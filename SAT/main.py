from generator import Generator

if __name__ == "__main__":
    generator = Generator("problem.config")
    sat, model_dimacs = generator.solve()
    generator.print_problem()
