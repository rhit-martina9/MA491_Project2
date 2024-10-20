import copy

def load_grid():
    grid = []
    with open("grid.txt") as file:
        for line in file:
            grid.append(line.replace("\n","").split(" "))
            for i in range(9):
                if grid[-1][i] == 'X':
                    grid[-1][i] = 0
                else:
                    grid[-1][i] = int(grid[-1][i])
    return grid

def get_row(num, grid):
    return grid[num-1]
def get_col(num, grid):
    return [row[num-1] for row in grid]
def get_box_coord(cell):
    row, col = cell
    return int(row / 3)*3 + int(col/3)
def get_box(num, grid):
    out = []
    base = (3*int(num/3),3*int(num%3))
    for row in range(3):
        for col in range(3):
            out.append(grid[base[0]+row][base[1]+col])
    return out

def get_candidates(cell, grid):
    candidates = [1,2,3,4,5,6,7,8,9]
    row, col = cell
    if grid[row][col] > 0:
        return []
    for i in range(9):
        if grid[i][col] in candidates:
            candidates.remove(grid[i][col])
    for j in range(9):
        if grid[row][j] in candidates:
            candidates.remove(grid[row][j])
    box = get_box(get_box_coord(cell), grid)
    for x in box:
        if x in candidates:
            candidates.remove(x)
    return candidates

def simple_steps(grid):
    new_grid = [['123456789' for j in range(9)] for i in range(9)]
    for row in range(9):
        for col in range(9):
            print('hi')
    return new_grid

grid = load_grid()
for line in grid:
    print(line)

print()
for row in range(9):
    for col in range(9):
        print(get_candidates((row,col), grid))
