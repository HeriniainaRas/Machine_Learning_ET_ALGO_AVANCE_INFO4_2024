
from heapq import heappush, heappop
import heapq
from nodes import Node

def manhattan_distance(grid, goal):
    dist = 0
    # Placer chaque élément de goal dans un dictionnaire avec ses coordonnées
    goal_positions = {}
    for i in range(len(goal)):
        for j in range(len(goal[i])):
            goal_positions[goal[i][j]] = (i, j)
    
    # Calculer la distance de Manhattan pour chaque élément
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if grid[i][j] != '':  # Ignorer la case vide
                goal_row, goal_col = goal_positions[grid[i][j]]
                dist += abs(i - goal_row) + abs(j - goal_col)
    
    return dist

def a_star(initial_grid):
    # Create the initial node from the starting grid
    start_node = Node(initial_grid)
    open_list = []  # Priority queue for A* (min-heap)
    heapq.heappush(open_list, start_node)
    closed_list = set()  # Set of visited nodes

    while open_list:
        current_node = heapq.heappop(open_list)

        # Check if the goal is reached
        if current_node.manhattan_distance() == 0:
            return reconstruct_path(current_node)

        closed_list.add(tuple(map(tuple, current_node.grid)))  # Mark this state as visited

        # Get possible moves (neighbors)
        neighbors = get_neighbors(current_node)
        for neighbor in neighbors:
            if tuple(map(tuple, neighbor.grid)) not in closed_list:
                heapq.heappush(open_list, neighbor)

    return None  # No solution found

def get_neighbors(node):
    neighbors = []
    empty_row, empty_col = node.empty_pos
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Up, Down, Left, Right

    for direction in directions:
        new_row, new_col = empty_row + direction[0], empty_col + direction[1]
        if 0 <= new_row < len(node.grid) and 0 <= new_col < len(node.grid[0]):
            # Swap the empty space with the adjacent tile
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
    return path[::-1]  # Return the path from start to goal
