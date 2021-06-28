from generatore import Generatore

if __name__ == "__main__":
    generatore = Generatore("problem.config")
    sat, _ = generatore.solve()
    generatore.print_problem()
