from final_state_generator import generate_final_state
from solver import solve
from parser_move import gen_mosse
from parser_cnf import convert_to_dimacs

num_mosse = generate_final_state()
gen_mosse(num_mosse)
convert_to_dimacs()
solve()
