from generator import Generator
import time

if __name__ == "__main__":

    # generate all the clauses describing the problem
    generator = Generator("problem.config")
    sat, model_dimacs = generator.solve()

    generator.print_problem()
