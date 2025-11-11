import numpy as np
import random
import heapq

def generate_random_maze(rows=10, cols=10, wall_prob=0.3, max_attempts=50):
    """Generate a random solvable maze using retries."""
    for _ in range(max_attempts):
        maze = (np.random.rand(rows, cols) < wall_prob).astype(int)
        maze[0, 0] = 0
        maze[rows - 1, cols - 1] = 0

        # Check solvability using Dijkstra
        path = dijkstra(maze, (0, 0), (rows - 1, cols - 1))
        if len(path) > 1:
            return maze  # ✅ solvable maze found

    # If no solvable maze found after all attempts, relax constraints
    print("⚠️ Could not find a solvable maze, returning last attempt.")
    return maze

def dijkstra(maze, start, goal):
    rows, cols = maze.shape
    directions = [(0,1),(1,0),(-1,0),(0,-1)]
    pq = [(0, start)]
    distances = {start: 0}
    prev = {}

    while pq:
        cost, current = heapq.heappop(pq)
        if current == goal:
            break
        for dr, dc in directions:
            nr, nc = current[0]+dr, current[1]+dc
            if 0 <= nr < rows and 0 <= nc < cols and maze[nr, nc] == 0:
                new_cost = cost + 1
                if (nr,nc) not in distances or new_cost < distances[(nr,nc)]:
                    distances[(nr,nc)] = new_cost
                    prev[(nr,nc)] = current
                    heapq.heappush(pq, (new_cost, (nr,nc)))

    path = []
    node = goal
    while node in prev:
        path.append(node)
        node = prev[node]
    path.append(start)
    path.reverse()
    return path
