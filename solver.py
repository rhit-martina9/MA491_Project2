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

def isrelated(cell1, cell2):
    if cell1[0] == cell2[0]:
        return 1
    if cell1[1] == cell2[1]:
        return 1
    if get_box_num(cell1) == get_box_num(cell2):
        return 1
    return 0
def find_xy_wings(grid):
    candidates = [[get_candidates((row,col),grid) for col in range(N)] for row in range(N)]
    xy_wings = []
    cells = [(r,c) for c in range(N) for r in range(N)]
    for i in range(N*N):
        for j in range(i+1,N*N):
            for k in range(j+1,N*N):
                if len(candidates[cells[i][0]][cells[i][1]]) != 2 or len(candidates[cells[j][0]][cells[j][1]]) != 2 or len(candidates[cells[k][0]][cells[k][1]]) != 2:
                    continue
                combined = sorted(candidates[cells[i][0]][cells[i][1]] + candidates[cells[j][0]][cells[j][1]] + candidates[cells[k][0]][cells[k][1]])
                if combined[0] == combined[1] and combined[2] == combined[3] and combined[4] == combined[5]:
                    if isrelated(cells[i], cells[j])+isrelated(cells[i], cells[k])+isrelated(cells[j], cells[k]) == 2:
                        xy_wings.append([cells[i], cells[j], cells[k]])
    return xy_wings

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
print()

wings = find_xy_wings(grid)
print(wings)
cands = [[get_candidates((row,col),grid) for col in range(N)] for row in range(N)]
print([[cands[cand[0]][cand[1]] for cand in wing] for wing in wings])
print(isrelated((1,1),(1,4)) + isrelated((1,1),(4,1)) + isrelated((1,4),(4,1)))
print(isrelated((1,1),(1,4)) + isrelated((2,0),(1,4)) + isrelated((1,1),(2,0)))
print(isrelated((1,1),(4,2)) + isrelated((2,0),(4,2)) + isrelated((1,1),(2,0)))