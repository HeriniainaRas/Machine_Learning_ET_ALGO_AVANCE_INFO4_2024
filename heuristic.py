def hamming_distance(grid, goal):
    """Compte le nombre de tuiles mal placées"""
    dist = 0
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if grid[i][j] != '' and grid[i][j] != goal[i][j]:
                dist += 1
    return dist

def euclidean_distance(grid, goal):
    """Calcule la distance euclidienne pour chaque tuile"""
    dist = 0
    goal_positions = {}
    for i in range(len(goal)):
        for j in range(len(goal[i])):
            goal_positions[goal[i][j]] = (i, j)
    
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if grid[i][j] != '':
                goal_row, goal_col = goal_positions[grid[i][j]]
                dist += np.sqrt((i - goal_row)**2 + (j - goal_col)**2)
    return dist

def linear_conflict(grid, goal):
    """Manhattan distance + pénalité pour les conflits linéaires"""
    base_dist = manhattan_distance(grid, goal)
    conflicts = 0
    
    # Vérifier les lignes
    for i in range(len(grid)):
        row_tiles = [(tile, j) for j, tile in enumerate(grid[i]) if tile != '']
        for k1 in range(len(row_tiles)):
            for k2 in range(k1+1, len(row_tiles)):
                tile1, pos1 = row_tiles[k1]
                tile2, pos2 = row_tiles[k2]
                if tile1 > tile2 and pos1 < pos2:
                    conflicts += 2
    
    return base_dist + conflicts

def manhattan_distance(grid, goal):
    dist = 0
    goal_positions = {}
    for i in range(len(goal)):
        for j in range(len(goal[i])):
            goal_positions[goal[i][j]] = (i, j)
    
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if grid[i][j] != '':
                goal_row, goal_col = goal_positions[grid[i][j]]
                dist += abs(i - goal_row) + abs(j - goal_col)
    
    return dist

def uniform_cost(grid, goal):
    return 0