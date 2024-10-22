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

def hidden_helper(hidden_groups, i, nums, want, all_cells, grid, found):
    if i > len(all_cells):
        return
    if len(nums) > 0 and nums[-1] in found:
        hidden_helper(hidden_groups, i+1,nums[:-1] + [i+1], want, all_cells, grid, found)
        return
    if len(nums) == want:
        # print(nums)
        cells = list(filter(lambda cell: any([num in grid[cell[0]][cell[1]] for num in nums]),all_cells))
        if len(cells) == want and cells not in hidden_groups:
            hidden_groups.append(cells)
        return
    else:
        hidden_helper(hidden_groups, i+1,nums + [i+1], want, all_cells, grid, found)
        hidden_helper(hidden_groups, i+1,nums, want, all_cells, grid, found)
def find_hidden_groups(c, grid):
    candidates = [[get_candidates((row,col),grid) for col in range(N)] for row in range(N)]
    hidden_groups = []
    for row in range(N):
        all_cells = [(row,col) for col in range(N)]
        hidden_helper(hidden_groups, 0, [], c, all_cells, candidates, [grid[cell[0]][cell[1]] for cell in all_cells])
    for col in range(N):
        all_cells = [(row,col) for row in range(N)]
        hidden_helper(hidden_groups, 0, [], c, all_cells, candidates, [grid[cell[0]][cell[1]] for cell in all_cells])
    for box in range(N):
        all_cells = get_box_cells(box)
        hidden_helper(hidden_groups, 0, [], c, all_cells, candidates, [grid[cell[0]][cell[1]] for cell in all_cells])
    return hidden_groups

def naked_helper(naked_groups, i, cells, want, all_cells, grid):
    if len(cells) == want:
        if cells not in naked_groups:
            naked_groups.append(cells)
        return
    if i == len(all_cells):
        return
    elif len(grid[all_cells[i][0]][all_cells[i][1]]) != want or (len(cells) > 0 and grid[cells[-1][0]][cells[-1][1]] != grid[all_cells[i][0]][all_cells[i][1]]):
        naked_helper(naked_groups, i+1,cells, want, all_cells, grid)
    else:
        naked_helper(naked_groups, i+1,cells + all_cells[i:i+1], want, all_cells, grid)
        naked_helper(naked_groups, i+1,cells, want, all_cells, grid)
def find_naked_groups(c, grid):
    candidates = [[get_candidates((row,col),grid) for col in range(N)] for row in range(N)]
    naked_groups = []
    for row in range(N):
        naked_helper(naked_groups, 0, [], c, [(row,col) for col in range(N)], candidates)
    if c > 1:
        for col in range(N):
            naked_helper(naked_groups, 0, [], c, [(row,col) for row in range(N)], candidates)
        for box in range(N):
            naked_helper(naked_groups, 0, [], c, get_box_cells(box), candidates)
    return naked_groups

grid = load_grid()
for line in grid:
    print(line)

# print()
# for row in range(N):
#     print([get_candidates((row,col), grid) for col in range(N)])

print()
# print(check_valid((0,6),1,grid))
# print()
# for row in range(N):
#     for col in range(N):
#         print(get_candidates((row,col),grid))
print(find_hidden_groups(1,grid))
print(find_hidden_groups(2,grid))
print(find_hidden_groups(3,grid))
print()
print(find_naked_groups(1,grid))
print(find_naked_groups(2,grid))
print(find_naked_groups(3,grid))