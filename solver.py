import copy
n = 3
N = n*n

def load_grid():
    grid = []
    with open("grid.txt") as file:
        for line in file:
            grid.append(line.replace("\n","").split(" "))
            for i in range(N):
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
    return int(row / n)*n + int(col/n)
def get_box_cells(box_num):
    out = []
    base = (box_num - box_num%n, n*(box_num%n))
    for row in range(n):
        for col in range(n):
            out.append((base[0]+row,base[1]+col))
    return out
def get_box_values(box_num, grid):
    return [grid[i][j] for i,j in get_box_cells(box_num)]

def check_valid(cell, num, grid):
    row, col = cell
    if grid[row][col] > 0:
        return False
    for i in range(N):
        if grid[i][col] == num:
            return False
    for i in range(N):
        if grid[row][i] == num:
            return False
    for x in get_box_values(get_box_num(cell), grid):
        if x == num:
            return False
    return True
def get_candidates(cell, grid):
    cands = [i+1 for i in range(N)]
    return list(filter(lambda v: check_valid(cell,v,grid), cands))
    
def find_number_locations(num, grid):
    locations = []
    for row in range(N):
        for col in range(N):
            if grid[row][col] == num:
                locations.append((row,col))
                continue
    return locations

def find_hidden_singles(grid):
    hidden_singles = {i+1:[] for i in range(N)}
    for num in range(1,10):
        for row in range(N):
            possible = list(filter(lambda cell: check_valid(cell, num, grid), [(row,col) for col in range(N)]))
            if len(possible) == 1 and possible[0] not in hidden_singles[num]:
                hidden_singles[num].append(possible[0])
        for col in range(N):
            possible = list(filter(lambda cell: check_valid(cell, num, grid), [(row,col) for row in range(N)]))
            if len(possible) == 1 and possible[0] not in hidden_singles[num]:
                hidden_singles[num].append(possible[0])
        for box_num in range(N):
            possible = list(filter(lambda cell: check_valid(cell, num, grid), get_box_cells(box_num)))
            if len(possible) == 1 and possible[0] not in hidden_singles[num]:
                hidden_singles[num].append(possible[0])
        hidden_singles[num] = sorted(hidden_singles[num], key=lambda v:v[0])
    return hidden_singles
def find_naked_singles(grid):
    candidates = [[get_candidates((r,c),grid) for c in range(N)] for r in range(N)]
    naked_singles = {i+1:[] for i in range(N)}
    for row in range(N):
        for col in range(N):
            cands = candidates[row][col]
            if len(cands) == 1:
                naked_singles[cands[0]].append((row,col))
    return naked_singles

def naked_helper(i, cells, want, all_cells, grid):
    if len(cells) == want:
        print(cells)
        return
    if i == len(all_cells):
        return
    elif len(grid[all_cells[i][0]][all_cells[i][1]]) != want or (len(cells) > 0 and grid[cells[-1][0]][cells[-1][1]] != grid[all_cells[i][0]][all_cells[i][1]]):
        naked_helper(i+1,cells, want, all_cells, grid)
    else:
        naked_helper(i+1,cells + all_cells[i:i+1], want, all_cells, grid)
        naked_helper(i+1,cells, want, all_cells, grid)

def find_naked_groups(c, grid):
    candidates = [[get_candidates((row,col),grid) for col in range(N)] for row in range(N)]
    # naked_groups = []
    for row in range(N):
        naked_helper(0, [], c, [(row,col) for col in range(9)], candidates)
    if c > 1:
        for col in range(N):
            naked_helper(0, [], c, [(row,col) for row in range(9)], candidates)
        for box in range(N):
            naked_helper(0, [], c, get_box_cells(box), candidates)
    

def find_naked_doubles(grid):
    candidates = [[get_candidates((row,col),grid) for col in range(N)] for row in range(N)]
    naked_doubles = []
    for row in range(N):
        for col1 in range(N):
            for col2 in range(col1+1,N):
                if candidates[row][col1] == candidates[row][col2] and len(candidates[row][col1]) == 2:
                    naked_doubles.append(((row,col1),(row,col2)))
    for col in range(N):
        for row1 in range(N):
            for row2 in range(row1+1,N):
                if candidates[row1][col] == candidates[row2][col] and len(candidates[row1][col]) == 2:
                    naked_doubles.append(((row1,col),(row2,col)))
    for box in range(N):
        box_coords = get_box_cells(box)
        for i in range(N):
            cell1 = box_coords[i]
            for j in range(i+1,N):
                cell2 = box_coords[j]
                if candidates[cell1[0]][cell1[1]] == candidates[cell2[0]][cell2[1]] and len(candidates[cell1[0]][cell1[1]]) == 2:
                    naked_doubles.append((cell1,cell2))
    return naked_doubles

def find_naked_triples(grid):
    candidates = [[get_candidates((row,col),grid) for col in range(N)] for row in range(N)]
    naked_triples = []
    for row in range(N):
        for col1 in range(N):
            for col2 in range(col1+1,N):
                for col3 in range(col2+1,N):
                    if candidates[row][col1] == candidates[row][col2] and candidates[row][col1] == candidates[row][col3] and len(candidates[row][col1]) == 3:
                        naked_triples.append(((row,col1),(row,col2),(row,col3)))
    for col in range(N):
        for row1 in range(N):
            for row2 in range(row1+1,N):
                for row3 in range(row2+1,N):
                    if candidates[row1][col] == candidates[row2][col] and candidates[row1][col] == candidates[row3][col] and len(candidates[row1][col]) == 3:
                        naked_triples.append(((row1,col),(row2,col),(row3,col)))
    for box in range(N):
        box_coords = get_box_cells(box)
        for i in range(N):
            cell1 = box_coords[i]
            for j in range(i+1,N):
                cell2 = box_coords[j]
                for k in range(j+1,N):
                    cell3 = box_coords[k]
                    if candidates[cell1[0]][cell1[1]] == candidates[cell2[0]][cell2[1]] and candidates[cell1[0]][cell1[1]] == candidates[cell3[0]][cell3[1]] and len(candidates[cell1[0]][cell1[1]]) == 3:
                        naked_triples.append((cell1,cell2,cell3))
    return naked_triples

grid = load_grid()
for line in grid:
    print(line)

print()
# print(check_valid((0,6),1,grid))
find_naked_groups(1,grid)
find_naked_groups(2,grid)
find_naked_groups(3,grid)
print()
# for row in range(N):
#     for col in range(N):
#         print(get_candidates((row,col),grid))
# print(find_hidden_singles(grid))
print(find_naked_singles(grid))
print(find_naked_doubles(grid))
print(find_naked_triples(grid))
