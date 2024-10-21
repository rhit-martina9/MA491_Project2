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
def get_box_num(cell):
    row, col = cell
    return int(row / 3)*3 + int(col/3)
def get_box_cells(box_num):
    out = []
    base = (box_num - box_num%3, 3*(box_num%3))
    for row in range(3):
        for col in range(3):
            out.append((base[0]+row,base[1]+col))
    return out
def get_box_values(box_num, grid):
    return [grid[i][j] for i,j in get_box_cells(box_num)]

def check_valid(cell, num, grid):
    row, col = cell
    if grid[row][col] > 0:
        return False
    for i in range(9):
        if grid[i][col] == num:
            return False
    for i in range(9):
        if grid[row][i] == num:
            return False
    for x in get_box_values(get_box_num(cell), grid):
        if x == num:
            return False
    return True
def get_candidates(cell, grid):
    cands = [i+1 for i in range(9)]
    return list(filter(lambda v: check_valid(cell,v,grid), cands))
    
def find_number_locations(num, grid):
    locations = []
    for row in range(9):
        for col in range(9):
            if grid[row][col] == num:
                locations.append((row,col))
                continue
    return locations

def find_hidden_singles(grid):
    hidden_singles = {i+1:[] for i in range(9)}
    for num in range(1,10):
        for row in range(9):
            possible = list(filter(lambda cell: check_valid(cell, num, grid), [(row,col) for col in range(9)]))
            if len(possible) == 1 and possible[0] not in hidden_singles[num]:
                hidden_singles[num].append(possible[0])
        for col in range(9):
            possible = list(filter(lambda cell: check_valid(cell, num, grid), [(row,col) for row in range(9)]))
            if len(possible) == 1 and possible[0] not in hidden_singles[num]:
                hidden_singles[num].append(possible[0])
        for box_num in range(9):
            possible = list(filter(lambda cell: check_valid(cell, num, grid), get_box_cells(box_num)))
            if len(possible) == 1 and possible[0] not in hidden_singles[num]:
                hidden_singles[num].append(possible[0])
        hidden_singles[num] = sorted(hidden_singles[num], key=lambda v:v[0])
    return hidden_singles

def find_naked_singles(grid):
    naked_singles = {i+1:[] for i in range(9)}
    for row in range(9):
        for col in range(9):
            cands = get_candidates((row,col), grid)
            if len(cands) == 1:
                naked_singles[cands[0]].append((row,col))
    return naked_singles

grid = load_grid()
for line in grid:
    print(line)

print()
# print(check_valid((0,6),1,grid))
# print()
# for row in range(9):
#     for col in range(9):
#         print(get_candidates((row,col),grid))
print(find_hidden_singles(grid))
print(find_naked_singles(grid))