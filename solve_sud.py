from pysat.formula import CNF
from pysat.solvers import Solver
import csv,time,sys


def sudoku_number(row,N):
    if(row<N*N):
        return 1
    if(row>=N*N):
        return 2


def v(N,sudoku_number,row,col,numb):
    if(sudoku_number==1):
        return ((N**4)*(numb-1))+((N*N)*row)+col+1
    if(sudoku_number==2):
        return (N**6)+(N**4)*(numb-1)+((N*N)*(row-N*N))+col+1


def solve_sudoku(grid,N):

    _cnf=CNF()

    for r in range(2*N*N):
        for c in range(N*N):
            if(grid[r][c]!=0):
                _cnf.append([v(N,sudoku_number(r,N),r,c,grid[r][c])])
                for n in range(1,N*N+1):
                    if(n!=grid[r][c]):
                        _cnf.append([-v(N,sudoku_number(r,N),r,c,n)])


    # any box contains at least one value
    for r in range(2*N*N):
        for c in range(N*N):
            _cnf.append([v(N,sudoku_number(r,N),r,c,n)for n in range(1,N*N+1)])


    # no same number in any column
    for r in range(2*N*N):
        for n in range(1,N*N+1):
            for cc in range(N*N-1):
                for ccc in range(cc+1,N*N):
                    _cnf.append([-v(N,sudoku_number(r,N),r,cc,n),-v(N,sudoku_number(r,N),r,ccc,n)])


    # no same number in any row
    for c in range(N*N):
        for n in range(1,N*N+1):
            for rr in range(N*N-1):
                for rrr in range(rr+1,N*N):
                    _cnf.append([-v(N,sudoku_number(rr,N),rr,c,n),-v(N,sudoku_number(rrr,N),rrr,c,n)])
            
            for rr in range(N*N,2*N*N-1):
                for rrr in range(rr+1,2*N*N):
                    _cnf.append([-v(N,sudoku_number(rr,N),rr,c,n),-v(N,sudoku_number(rrr,N),rrr,c,n)])


    # any N*N box contains unique values
    for r in range(2*N):
        for c in range(N):
            from_r=r*N
            from_c=c*N
            haha=[i for i in range(N*N)]
            for n in range(1,N*N+1):
                for to_r in range(from_r,from_r+N):
                    for to_c in range(from_c,from_c+N):
                        haha[(to_r-from_r)*N+(to_c-from_c)]=v(N,sudoku_number(to_r,N),to_r,to_c,n)

                for i in range(0,N*N-1):
                    for j in range(i+1,N*N):
                        _cnf.append([-haha[i],-haha[j]])
            

            
    # sudokus contain unique pair of values or not
    for r in range(N*N):
        for c in range(N*N):
            for n in range(1,N*N+1):
                _cnf.append([-v(N,sudoku_number(r,N),r,c,n),-v(N,sudoku_number(r+N*N,N),r+N*N,c,n)])
    

    # solve the given clauses
    s=Solver(bootstrap_with=_cnf.clauses)
    s.solve()

    if(s.get_model()==None):
        return []
    else:
        clause_model=list(s.get_model())
        ans=[[0 for i in range(N*N)] for j in range(2*N*N)]
        
        for r in range(2*N*N):
            for c in range(N*N):
                for n in range(1,N*N+1):
                    if(clause_model[v(N,sudoku_number(r,N),r,c,n)-1]>0):
                        ans[r][c]=n


    s.delete()
    return ans


def main():
    if len(sys.argv) != 2:
        print("Required arguments: puzzle dimension")
        exit(1)

    try:
        N = int(sys.argv[1])
    except:
        print("Cannot parse",sys.argv[1],"as integer")
        exit(1)


    file_name = "input_a/input_" + str(N) + ".csv"
    grid=list(csv.reader(open(file_name)))
    # input from csv file is in str form
    for r in range(2*N*N):
        for c in range(N*N):
            grid[r][c]=int(grid[r][c])


    #time() to measure the time taken to solve the 2 sudokus
    start = time.time()
    #take answer in already declared grid
    grid = solve_sudoku(grid,N)
    end = time.time()
    if grid:
        print("Time: "+str(end - start))

    #write the combined grid to the csv file
    file_name = "output_a/output_" + str(N) + ".csv" 
    with open(file_name, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(grid)


if __name__ == '__main__':
    main()