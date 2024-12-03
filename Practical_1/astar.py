import pygame
import math
from queues import PrioQueue

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

WIDTH = 22
HEIGHT = 22
MARGIN = 3

SCREEN_WIDTH, SCREEN_HEIGHT = 504, 504


class Field:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.color = WHITE
        self.walkable = True
        self.cost = 0

    def __lt__(self, other: 'Field') -> bool:
        return self.cost < other.cost


class Grid:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.fields = [[Field(x, y) for y in range(height)] for x in range(width)]

    def create_wall(self, start, end):
        if isinstance(start, tuple) and len(start) == 2 and isinstance(end, tuple) and len(end) == 2:
            start_x, start_y = start
            end_x, end_y = end
            if start == end:
                self.fields[start_x][start_y].walkable = False
                self.fields[start_x][start_y].color = BLACK
            elif start_x == end_x:
                diff = abs(start_y - end_y) + 1
                index = min(start_y, end_y)
                for i in range(index, index + diff):
                    self.fields[start_x][i].walkable = False
                    self.fields[start_x][i].color = BLACK
            elif start_y == end_y:
                diff = abs(start_x - end_x) + 1
                index = min(start_x, end_x)
                for i in range(index, index + diff):
                    self.fields[i][start_y].walkable = False
                    self.fields[i][start_y].color = BLACK


class Drawer:
    def __init__(self, screen: pygame.Surface):
        self.screen = screen

    def draw(self, grid: Grid, color, field: Field):
        pygame.draw.rect(self.screen, color,
                         [(MARGIN + WIDTH) * field.x + MARGIN,
                          SCREEN_HEIGHT - ((MARGIN + HEIGHT) * field.y + MARGIN + HEIGHT),
                          WIDTH, HEIGHT])

    def draw_grid(self, grid: Grid):
        for row in grid.fields:
            for field in row:
                self.draw(grid, field.color, field)


def heuristic(a: Field, b: Field) -> float:
    return math.sqrt((a.x - b.x) ** 2 + (a.y - b.y) ** 2)


def get_neighbors(grid: Grid, field: Field) -> list:
    neighbors = []
    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        x, y = field.x + dx, field.y + dy
        if 0 <= x < grid.width and 0 <= y < grid.height:
            neighbors.append(grid.fields[x][y])
    return neighbors


def get_path(came_from: dict, current: Field) -> list:
    path = [current]
    while current in came_from:
        current = came_from[current]
        path.append(current)
    return path[::-1]


def a_star(grid: Grid, start: Field, goal: Field) -> list:
    frontier = PrioQueue()
    frontier.enqueue(start, 0)
    came_from = {}
    start.cost = 0
    explored = []

    while not frontier.is_empty():
        current = frontier.dequeue()
        explored.append(current)

        if current == goal:
            return get_path(came_from, current)

        new_cost = current.cost + 1

        for neighbor in get_neighbors(grid, current):
            if not neighbor.walkable or neighbor in explored:
                continue

            if new_cost < neighbor.cost or neighbor not in came_from:
                came_from[neighbor] = current
                neighbor.cost = new_cost
                priority = new_cost + heuristic(neighbor, goal)
                frontier.enqueue(neighbor, priority)

    return []


pygame.init()

size = (500, 500)
screen = pygame.display.set_mode(size)

pygame.display.set_caption("My Game")

done = False

clock = pygame.time.Clock()

grid = Grid(20, 20)
drawer = Drawer(screen)
grid.create_wall((9, 0), (9, 9))
grid.create_wall((9, 9), (4, 9))
grid.create_wall((16, 9), (16, 19))

start = grid.fields[0][0]
goal = grid.fields[19][19]

path = a_star(grid, start, goal)

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    screen.fill(BLACK)
    drawer.draw_grid(grid)

    for field in path:
        drawer.draw(grid, GREEN, field)

    drawer.draw(grid, RED, start)
    drawer.draw(grid, RED, goal)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
