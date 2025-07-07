from heapq import heappush, heappop
import heapq
from nodes import Node

from heuristic import manhattan_distance

def get_possible_swaps(grid):
    swaps = []
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            for x in range(i, len(grid)):
                for y in range(len(grid[x])):
                    if (i, j) != (x, y) and grid[i][j] != '' and grid[x][y] != '':
                        new_grid = [row.copy() for row in grid]
                        new_grid[i][j], new_grid[x][y] = new_grid[x][y], new_grid[i][j]
                        swaps.append(new_grid)
    return swaps

def a_star(initial_grid, k=3):
    start_node = Node(initial_grid)
    open_list = []
    heapq.heappush(open_list, start_node)
    closed_list = set()
    
    while open_list:
        current_node = heapq.heappop(open_list)
        
        if current_node.manhattan_distance() == 0:
            return reconstruct_path(current_node)
            
        current_state = tuple(map(tuple, current_node.grid))
        if current_state in closed_list:
            continue
            
        closed_list.add(current_state)
        
        # Obtenir les voisins normaux
        neighbors = get_neighbors(current_node)

        # Appliquer k-swap si nécessaire
        if k > 0 and current_node.move > 0 and current_node.move % k == 0:
            swap_neighbors = []
            possible_swaps = get_possible_swaps(current_node.grid)
            for swap_grid in possible_swaps:
                swap_node = Node(swap_grid, parent=current_node, move=current_node.move + 1)
                swap_neighbors.append(swap_node)
            neighbors.extend(swap_neighbors)

        for neighbor in neighbors:
            neighbor_state = tuple(map(tuple, neighbor.grid))
            if neighbor_state not in closed_list:
                heapq.heappush(open_list, neighbor)
    
    return None

def get_neighbors(node):
    neighbors = []
    empty_row, empty_col = node.empty_pos
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    for direction in directions:
        new_row, new_col = empty_row + direction[0], empty_col + direction[1]
        if 0 <= new_row < len(node.grid) and 0 <= new_col < len(node.grid[0]):
            new_grid = [row.copy() for row in node.grid]
            new_grid[empty_row][empty_col], new_grid[new_row][new_col] = new_grid[new_row][new_col], new_grid[empty_row][empty_col]
            neighbor = Node(new_grid, parent=node, move=node.move + 1)
            neighbors.append(neighbor)

    return neighbors

def reconstruct_path(node):
    path = []
    while node:
        path.append(node.grid)
        node = node.parent
    return path[::-1]