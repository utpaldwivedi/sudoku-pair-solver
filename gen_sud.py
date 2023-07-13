import numpy,csv
import pysat
import random
import sys,time
from pysat.card import *
from pysat.solvers import MinisatGH as Solver
from pysat.formula import CNF


nv = 0

def getVar():
        global nv 
        nv += 1
        return nv


def gen_sud(N):

    _cnf = CNF()

    # reshape to (N*N,N*N,N*N)
    def group_by(k, l):
        for i in range(len(l)//k):
            yield l[i*k:(i+1)*k]


    # create a variable for each choice of value (1..N*N) for each cell (1..N*N*N*N)
    V_init = [getVar() for v in range((N*N)**3)]

    # shuffle variables to randomize the generated solution everytime
    random.shuffle(V_init)

    V = list(group_by(N*N, list(group_by(N*N, V_init))))

    # Index of last solution variable (rest are added by cardinality encodings)
    global nv
    max_problem_var = nv

    _encoding = EncType.ladder

    #encode constraints for each column
    for i in range(N*N):
        for v in range(N*N):
            #atleast 1 clause
            col = [V[i][j][v] for j in range(N*N)]
            _cnf.append(col)
            #atmost 1 encoding
            _card = pysat.card.CardEnc.atmost(lits=col, top_id=nv, bound=1, encoding=_encoding)
            _cnf.extend(_card.clauses)
            nv = _card.nv

    #encode constraints for each row
    for j in range(N*N):
        for v in range(N*N):
            #atleast 1 clause
            row = [V[i][j][v] for i in range(N*N)]
            _cnf.append(row)
            #atmost 1 encoding
            _card = pysat.card.CardEnc.atmost(lits=row, top_id=nv, bound=1, encoding=_encoding)
            _cnf.extend(_card.clauses)
            nv = _card.nv

    #encode constraints for each square
    for xi in range(N):
        for xj in range(N):
            for v in range(N*N):
                #atleast 1 clause
                _block = [V[i][j][v] for i in range(xi*N,xi*N+N) for j in range(xj*N,xj*N+N)]
                _cnf.append(_block)
                #atmost 1 encoding
                _card = pysat.card.CardEnc.atmost(lits=_block, top_id=nv, bound=1, encoding=_encoding)
                _cnf.extend(_card.clauses)
                nv = _card.nv

    #encode constraints for each cell
    for i in range(N*N):
        for j in range(N*N):
            #atleast 1 clause
            _cnf.append(V[i][j]) 
            #atmost 1 encoding
            _card = pysat.card.CardEnc.atmost(lits=V[i][j], top_id=nv, bound=1, encoding=_encoding)
            _cnf.extend(_card.clauses)
            nv = _card.nv

    solver = Solver(bootstrap_with=_cnf.clauses)

    #first find a solution
    if solver.solve():
        _solution = [v for v in solver.get_model() if v > 0 and v <= max_problem_var]
        S = set(_solution)
        for i in range(N*N):
            for j in range(N*N):
                vs = V[i][j]
                true_sols = [ix+1 for (ix,v) in enumerate(vs) if v in S]

    
    #then try to find an alternate solution (by forbidding original with a clause)
    solver.add_clause([-v for v in _solution])

    untested_clues = _solution[:]
    #again shuffle to randomize the generation
    random.shuffle(untested_clues)

    necessary_clues = []

    solver.set_phases(v * random.randint(0,1)*2-1 for v in V_init)

    #compute minimum set of clues
    while len(untested_clues):

        test_clue = untested_clues.pop()

        if solver.solve(assumptions=necessary_clues+untested_clues):
            #alternate solution exists, so keep test_clue 
            necessary_clues.append(test_clue)        
        else:
            #now, no alternate solutions, so drop test_clue
            _core = solver.get_core()
            #remove clues unnecessary for deriving unsatisfiability
            untested_clues = [l for l in untested_clues if l in _core]

    #initialize the answer grid (N*N)
    grid = numpy.zeros((N*N,N*N),numpy.int64)

    #assign 0 or n in range(1,N*N+1) to the grid
    necessary_clues = set(necessary_clues)
    for i in range(N*N):
        for j in range(N*N):
            _v = V[i][j]
            true_sols = [ix+1 for (ix,v) in enumerate(_v) if v in necessary_clues]
            if len(true_sols):
                grid[i][j] = true_sols[0]
            else:
                grid[i][j] = 0


    #finally return the generated grid
    return grid


def main():
    if len(sys.argv) != 2:
        print("Required arguments: puzzle dimension")
        exit(1)

    try:
        N = int(sys.argv[1])
    except:
        print("Cannot parse",sys.argv[1],"as integer")
        exit(1)

    #time() to measure the time taken to generate
    start = time.time()
    #generating 2 grids
    grid_1 = gen_sud(N)
    grid_2 = gen_sud(N)
    end = time.time()
    print("Time: "+str(end - start))

    #write the 1st grid to csv file
    with open("output_b/output.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(grid_1)
    
    #append the 2nd grid to csv file
    with open("output_b/output.csv", "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(grid_2)


if __name__ == '__main__':
    main()