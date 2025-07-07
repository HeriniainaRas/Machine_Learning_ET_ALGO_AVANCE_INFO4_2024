import heapq

class Node:
    def __init__(self, grid, parent=None, move=0):
        self.grid = grid  # Current state of the puzzle
        self.parent = parent  # Parent node (to reconstruct path)
        self.move = move  # Number of moves taken to reach this state
        self.empty_pos = self.find_empty()  # Find the position of the empty tile
        self.cost = self.calculate_cost()  # Cost to reach this state (g(n))
        self.heuristic = self.manhattan_distance()  # Heuristic (h(n))
        self.f = self.cost + self.heuristic  # f(n) = g(n) + h(n)

    def find_empty(self):
        for i in range(len(self.grid)):
            for j in range(len(self.grid[i])):
                if self.grid[i][j] == "":
                    return i, j
        return None

    def calculate_cost(self):
        # g(n) is the number of moves from the initial state to the current state
        return self.move

    def manhattan_distance(self):
        # Heuristic function: Manhattan distance
        dist = 0
        goal = list(range(1, len(self.grid) * len(self.grid[0]))) + [""]
        for i in range(len(self.grid)):
            for j in range(len(self.grid[i])):
                if self.grid[i][j] != "":
                    goal_pos = goal.index(self.grid[i][j])
                    goal_row, goal_col = goal_pos // len(self.grid), goal_pos % len(self.grid[0])
                    dist += abs(i - goal_row) + abs(j - goal_col)
        return dist

    def __lt__(self, other):
        return self.f < other.f

    def __repr__(self):
        return f"Node(f={self.f}, move={self.move})"
