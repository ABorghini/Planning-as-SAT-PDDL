from final_state_generator import generate_final_state
from solver import solve
from moves_generator import gen_moves
from problem_generator import problem_gen
from convert2dimacs import convert_to_dimacs

num_mosse = generate_final_state()
gen_moves(num_mosse)
problem_gen()
convert_to_dimacs()
solve()



