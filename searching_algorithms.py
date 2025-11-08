from itertools import count
from operator import truediv

from utils import *
from collections import deque
from queue import PriorityQueue
from grid import Grid
from spot import Spot

def bfs(draw: callable, grid: Grid, start: Spot, end: Spot) -> bool:
    """
    Breadth-First Search (BFS) Algorithm.
    Args:
        draw (callable): A function to call to update the Pygame window.
        grid (Grid): The Grid object containing the spots.
        start (Spot): The starting spot.
        end (Spot): The ending spot.
    Returns:
        bool: True if a path is found, False otherwise.
    """

    queue = deque()
    queue.append(start)
    visited = {start}
    path = {}

    while queue:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = queue.popleft()

        if current == end:
            while current in path:
                current = path[current]
                current.make_path()
                draw()
            end.make_end()
            start.make_start()
            return True

        for neighbor in current.neighbors:
            if neighbor not in visited and not neighbor.is_barrier():
                visited.add(neighbor)
                path[neighbor] = current
                queue.append(neighbor)
                neighbor.make_open()

        draw()

        if current != start:
            current.make_closed()

    return False


def dfs(draw: callable, grid: Grid, start: Spot, end: Spot) -> bool:
    """
    Depdth-First Search (DFS) Algorithm.
    Args:
        draw (callable): A function to call to update the Pygame window.
        grid (Grid): The Grid object containing the spots.
        start (Spot): The starting spot.
        end (Spot): The ending spot.
    Returns:
        bool: True if a path is found, False otherwise.
    """

    if start is None or end is None:
        return False

    stack = [start]
    visited = {start}
    path = {}

    while stack:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = stack.pop()

        if current == end:
            while current in path:
                current = path[current]
                current.make_path()
                draw()
            end.make_end()
            start.make_start()
            return True

        for neighbor in current.neighbors:
            if neighbor not in visited and not neighbor.is_barrier():
                visited.add(neighbor)
                path[neighbor] = current
                stack.append(neighbor)
                neighbor.make_open()

        draw()

        if current != start:
            current.make_closed()

    return False



def h_manhattan_distance(p1: tuple[int, int], p2: tuple[int, int]) -> float:
    """
    Heuristic function for A* algorithm: uses the Manhattan distance between two points.
    Args:
        p1 (tuple[int, int]): The first point (x1, y1).
        p2 (tuple[int, int]): The second point (x2, y2).
    Returns:
        float: The Manhattan distance between p1 and p2.
    """
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)


def h_euclidian_distance(p1: tuple[int, int], p2: tuple[int, int]) -> float:
    """
    Heuristic function for A* algorithm: uses the Euclidian distance between two points.
    Args:
        p1 (tuple[int, int]): The first point (x1, y1).
        p2 (tuple[int, int]): The second point (x2, y2).
    Returns:
        float: The Manhattan distance between p1 and p2.
    """
    x1, y1 = p1
    x2, y2 = p2
    return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5



def astar(draw: callable, grid: Grid, start: Spot, end: Spot) -> bool:
    """
    A* Pathfinding Algorithm.
    Args:
        draw (callable): A function to call to update the Pygame window.
        grid (Grid): The Grid object containing the spots.
        start (Spot): The starting spot.
        end (Spot): The ending spot.
    Returns:
        bool: True if a path is found, False otherwise.
    """
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    open_set_hash = {start}

    came_from = {}

    g_score = {spot: float("inf") for row in grid.grid for spot in row}
    f_score = {spot: float("inf") for row in grid.grid for spot in row}
    g_score[start] = 0
    f_score[start] = h_manhattan_distance(start.get_position(), end.get_position())

    while not open_set.empty():

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False

        current = open_set.get()[2]
        open_set_hash.remove(current)

        if current == end:
            while current in came_from:
                current = came_from[current]
                current.make_path()
                draw()
            end.make_end()
            start.make_start()
            return True

        for neighbor in current.neighbors:
            temp_g_score = g_score[current] + 1

            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score + h_manhattan_distance(neighbor.get_position(), end.get_position())

                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.make_open()

        draw()

        if current != start:
            current.make_closed()

    return False

def dls(draw: callable, grid: Grid, start: Spot, end: Spot, depth_limit: int) -> bool:
    visited = {start}
    stack = [(start, 0)]
    path = {}

    while stack:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False

        current, depth = stack.pop()

        if current == end:
            while current in path:
                current = path[current]
                current.make_path()
                draw()
            end.make_end()
            start.make_start()
            return True

        if depth < depth_limit:
            for neighbor in current.neighbors:
                if neighbor not in visited and not neighbor.is_barrier():
                    visited.add(neighbor)
                    path[neighbor] = current
                    stack.append((neighbor, depth + 1))
                    neighbor.make_open()

        draw()

        if current != start:
            current.make_closed()

    return False


def ucs(draw: callable, grid: Grid, start: Spot, end: Spot) -> bool:

    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    open_set_hash = {start}

    came_from = {}
    cost = {spot: float("inf") for row in grid.grid for spot in row}
    cost[start] = 0

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False

        current_cost, _,  current = open_set.get()
        open_set_hash.remove(current)

        if current == end:
            while current in came_from:
                current = came_from[current]
                current.make_path()
                draw()
            end.make_end()
            start.make_start()
            return True

        for neighbor in current.neighbors:
            new_cost = cost[current] + 1

            if new_cost < cost[neighbor]:
                came_from[neighbor] = current
                cost[neighbor] = new_cost

                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((new_cost, count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.make_open()
        draw()

        if current != start:
            current.make_closed()
    return False

def dijkstra(draw: callable, grid: Grid, start: Spot, end: Spot) -> bool:
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    open_set_hash = {start}

    came_from = {}
    distance = {spot: float("inf") for row in grid.grid for spot in row}
    distance[start] = 0

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False

        current_distance, _, current = open_set.get()
        open_set_hash.remove(current)

        if current == end:
            while current in came_from:
                current = came_from[current]
                current.make_path()
                draw()
            end.make_end()
            start.make_start()
            return True

        for neighbor in current.neighbors:
            new_distance = distance[current] + 1
            if new_distance < distance[neighbor]:
                came_from[neighbor] = current
                distance[neighbor] = new_distance

                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((new_distance, count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.make_open()

        draw()

        if current != start:
            current.make_closed()

    return False


def iddfs(draw: callable, grid: Grid, start: Spot, end: Spot, depth_limit: int) -> bool:
    for limit in range(depth_limit):
        if dls(draw, grid, start, end, limit):
            return True

    return False


def ida(draw: callable, grid: Grid, start: Spot, end: Spot) -> bool:
    threshold = h_manhattan_distance(start.get_position(), end.get_position())

    while threshold < float("inf"):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False

        for row in grid.grid:
            for spot in row:
                if not spot.is_barrier() and spot != start and spot != end:
                    spot.reset()

        min_threshold = float("inf")
        stack = [(start, {start}, 0, [start])]
        found = False
        result_path = []

        while stack:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return False

            current, path_set, g, path = stack.pop()

            f = g + h_manhattan_distance(current.get_position(), end.get_position())

            if f > threshold:
                min_threshold = min(min_threshold, f)
                continue

            if current == end:
                found = True
                result_path = path
                break

            if current != start:
                current.make_closed()


            neighbors = list(current.neighbors)
            for neighbor in reversed(neighbors):
                if neighbor not in path_set and not neighbor.is_barrier():
                    new_path_set = path_set | {neighbor}
                    stack.append((neighbor, new_path_set, g + 1, path + [neighbor]))

                    if neighbor != end:
                        neighbor.make_open()

            draw()

        if found and result_path:
            for spot in result_path:
                spot.make_path()
            draw()
            end.make_end()
            start.make_start()
            return True

        if min_threshold == float("inf"):
            return False

        threshold = min_threshold

    return False


# and the others algorithms...
# ▢ Depth-Limited Search (DLS)
# ▢ Uninformed Cost Search (UCS)
# ▢ Greedy Search (Dijkstra)
# ▢ Iterative Deepening Search/Iterative Deepening Depth-First Search (IDS/IDDFS)
# ▢ Iterative Deepening A* (IDA)
# Assume that each edge (graph weight) equals