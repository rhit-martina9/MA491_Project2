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
    return grid[num]
def get_col(num, grid):
    return [row[num] for row in grid]
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
def get_relation(cell1, cell2):
    out = []
    if cell1[0] == cell2[0]:
        out.append(1)
    if cell1[1] == cell2[1]:
        out.append(2)
    if get_box_num(cell1) == get_box_num(cell2):
        out.append(3)
    return out

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
        cells = list(filter(lambda cell: any([num in grid[cell[0]][cell[1]] for num in nums]),all_cells))
        if len(cells) == want:
            key = ''.join([str(num) for num in nums])
            if key not in hidden_groups:
                hidden_groups[key] = []
            if cells not in hidden_groups[key]:
                hidden_groups[key].append(cells)
        return
    else:
        hidden_helper(hidden_groups, i+1,nums + [i+1], want, all_cells, grid, found)
        hidden_helper(hidden_groups, i+1,nums, want, all_cells, grid, found)
def find_hidden_groups(c, grid, candidates=[]):
    if candidates == []:
        candidates = [[get_candidates((row,col),grid) for col in range(N)] for row in range(N)]
    hidden_groups = {}
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
def apply_hidden_groups_move(group, group_values, candidates, grid):
    new_grid = [[col for col in row] for row in grid]
    new_cands = [[col for col in row] for row in candidates]
    int_values = [int(group_values[i]) for i in range(len(group_values))]
    if len(group) == 1:
        new_grid[group[0][0]][group[0][1]] = int_values[0]
        new_cands[group[0][0]][group[0][1]] = []
        for row in range(N):
            if int_values[0] in new_cands[row][group[0][1]]:
                new_cands[row][group[0][1]].remove(int_values[0])
        for col in range(N):
            if int_values[0] in new_cands[group[0][0]][col]:
                new_cands[group[0][0]][col].remove(int_values[0])
        for cell in get_box_cells(get_box_num(group[0])):
            if int_values[0] in new_cands[cell[0]][cell[1]]:
                new_cands[cell[0]][cell[1]].remove(int_values[0])
    else:
        if all([1 in get_relation(group[0],g) for g in group]):
            for col in range(N):
                if (group[0][0], col) in group:
                    new_cands[group[0][0]][col] = [x for x in new_cands[group[0][0]][col] if x in int_values]
                else:
                    new_cands[group[0][0]][col] = [x for x in new_cands[group[0][0]][col] if x not in int_values]
        if all([2 in get_relation(group[0],g) for g in group]):
            for row in range(N):
                if (row, group[0][1]) in group:
                    new_cands[row][group[0][1]] = [x for x in new_cands[row][group[0][1]] if x in int_values]
                else:
                    new_cands[row][group[0][1]] = [x for x in new_cands[row][group[0][1]] if x not in int_values]
        if all([3 in get_relation(group[0],g) for g in group]):
            for cell in get_box_cells(get_box_num(group[0])):
                if cell in group:
                    new_cands[cell[0]][cell[1]] = [x for x in new_cands[cell[0]][cell[1]] if x in int_values]
                else:
                    new_cands[cell[0]][cell[1]] = [x for x in new_cands[cell[0]][cell[1]] if x not in int_values]
    return new_grid, new_cands

def naked_helper(naked_groups, i, nums, want, all_cells, grid, found):
    if i > len(all_cells):
        return
    if len(nums) > 0 and nums[-1] in found:
        naked_helper(naked_groups, i+1,nums[:-1] + [i+1], want, all_cells, grid, found)
        return
    if len(nums) == want:
        cells = list(filter(lambda cell: grid[cell[0]][cell[1]] != [] and all([num in nums for num in grid[cell[0]][cell[1]]]),all_cells))
        if len(cells) == want:
            key = ''.join([str(num) for num in nums])
            if key not in naked_groups:
                naked_groups[key] = []
            if cells not in naked_groups[key]:
                naked_groups[key].append(cells)
        return
    else:
        naked_helper(naked_groups, i+1,nums + [i+1], want, all_cells, grid, found)
        naked_helper(naked_groups, i+1,nums, want, all_cells, grid, found)
def find_naked_groups(c, grid, candidates=[]):
    if candidates == []:
        candidates = [[get_candidates((row,col),grid) for col in range(N)] for row in range(N)]
    naked_groups = {}
    for row in range(N):
        all_cells = [(row,col) for col in range(N)]
        naked_helper(naked_groups, 0, [], c, all_cells, candidates, [grid[cell[0]][cell[1]] for cell in all_cells])
    for col in range(N):
        all_cells = [(row,col) for row in range(N)]
        naked_helper(naked_groups, 0, [], c, all_cells, candidates, [grid[cell[0]][cell[1]] for cell in all_cells])
    for box in range(N):
        all_cells = get_box_cells(box)
        naked_helper(naked_groups, 0, [], c, all_cells, candidates, [grid[cell[0]][cell[1]] for cell in all_cells])
    return naked_groups
def apply_naked_groups_move(group, group_values, candidates, grid):
    new_grid = [[col for col in row] for row in grid]
    new_cands = [[col for col in row] for row in candidates]
    int_values = [int(group_values[i]) for i in range(len(group_values))]
    if len(group) == 1:
        new_grid[group[0][0]][group[0][1]] = int_values[0]
        new_cands[group[0][0]][group[0][1]] = []
        for row in range(N):
            if int_values[0] in new_cands[row][group[0][1]]:
                new_cands[row][group[0][1]].remove(int_values[0])
        for col in range(N):
            if int_values[0] in new_cands[group[0][0]][col]:
                new_cands[group[0][0]][col].remove(int_values[0])
        for cell in get_box_cells(get_box_num(group[0])):
            if int_values[0] in new_cands[cell[0]][cell[1]]:
                new_cands[cell[0]][cell[1]].remove(int_values[0])
    else:
        if all([1 in get_relation(group[0],g) for g in group]):
            for col in range(N):
                if (group[0][0], col) not in group:
                    new_cands[group[0][0]][col] = [x for x in new_cands[group[0][0]][col] if x not in int_values]
        if all([2 in get_relation(group[0],g) for g in group]):
            for row in range(N):
                if (row, group[0][1]) not in group:
                    new_cands[row][group[0][1]] = [x for x in new_cands[row][group[0][1]] if x not in int_values]
        if all([3 in get_relation(group[0],g) for g in group]):
            for cell in get_box_cells(get_box_num(group[0])):
                if cell not in group:
                    new_cands[cell[0]][cell[1]] = [x for x in new_cands[cell[0]][cell[1]] if x not in int_values]
    return new_grid, new_cands

def isrelated(cell1, cell2):
    return 1 if get_relation(cell1,cell2)!=[] else 0
def find_xy_wings(grid, candidates=[]):
    if candidates == []:
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
def apply_xy_wings(candidates,grid):
    pass

def display_grid(grid):
    for line in grid:
        print(line)
    print()
def display_candidates(candidates, grid):
    for row in range(N):
        for col in range(N):
            cand_str = f"[{''.join([str(num) for num in candidates[row][col]])}]"
            if cand_str == "[]":
                cand_str = str(grid[row][col])
            print("{0:^9s}".format(cand_str), end=" ")
        print()

grid = load_grid()
cands = [[get_candidates((row,col),grid) for col in range(N)] for row in range(N)]
display_grid(grid)
display_candidates(cands, grid)

print()
# print(find_hidden_groups(1,grid))
# print(find_hidden_groups(2,grid))
# print(find_hidden_groups(3,grid))
# print()
print(find_naked_groups(1,grid))
print(find_naked_groups(2,grid))
print(find_naked_groups(3,grid))
# print()

# wings = find_xy_wings(grid)
# print(wings)
# print([[cands[cand[0]][cand[1]] for cand in wing] for wing in wings])


print()
new_grid = grid
new_cands = cands

naked_groups = find_naked_groups(1,new_grid,new_cands)
count = 1
while naked_groups != {} or count > 0:
    for i in range(1,10):
        for num in naked_groups:
            for j in range(len(naked_groups[num])):
                new_grid, new_cands = apply_naked_groups_move(naked_groups[num][j], num, new_cands, new_grid)
        naked_groups = find_naked_groups((i%9)+1,new_grid,new_cands)
    count -= 1

display_grid(new_grid)
display_candidates(new_cands, new_grid)
print()
print(find_naked_groups(1,new_grid,new_cands))
print(find_naked_groups(2,new_grid,new_cands))
print(find_naked_groups(3,new_grid,new_cands))

# hidden_groups = find_hidden_groups(1,new_grid,new_cands)
# while hidden_groups != {}:
#     for i in range(1,10):
#         for num in hidden_groups:
#             for j in range(len(hidden_groups[num])):
#                 new_grid, new_cands = apply_hidden_groups_move(hidden_groups[num][j], num, new_cands, new_grid)
#         hidden_groups = find_hidden_groups((i%9)+1,new_grid,new_cands)

# display_grid(new_grid)
# display_candidates(new_cands, new_grid)
# print()
# print(find_hidden_groups(1,new_grid,new_cands))
# print(find_hidden_groups(2,new_grid,new_cands))
# print(find_hidden_groups(3,new_grid,new_cands))