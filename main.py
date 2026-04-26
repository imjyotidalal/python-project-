import pygame
import random
import math

# ---------------- SETTINGS ----------------
WIDTH, HEIGHT = 900, 700
NUM_AGENTS = 100

NEIGHBOR_RADIUS = 50
SEPARATION_RADIUS = 20

# -----------------------------------------

def distance(a, b):
    return math.sqrt((a.x - b.x)**2 + (a.y - b.y)**2)

def limit_vector(x, y, max_val):
    mag = math.sqrt(x*x + y*y)
    if mag > max_val:
        return (x/mag)*max_val, (y/mag)*max_val
    return x, y

# ---------------- AGENT CLASS ----------------
class Agent:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vx = random.uniform(-1, 1)
        self.vy = random.uniform(-1, 1)
        self.max_speed = 2
        self.panic = False

    def update(self, agents, goal, obstacles):
        sep_x, sep_y = 0, 0
        ali_x, ali_y = 0, 0
        coh_x, coh_y = 0, 0

        count = 0

        for other in agents:
            if other != self:
                d = distance(self, other)

                # Separation
                if d < SEPARATION_RADIUS and d > 0:
                    sep_x += (self.x - other.x) / d
                    sep_y += (self.y - other.y) / d

                # Alignment & Cohesion
                if d < NEIGHBOR_RADIUS:
                    ali_x += other.vx
                    ali_y += other.vy
                    coh_x += other.x
                    coh_y += other.y
                    count += 1

        if count > 0:
            ali_x /= count
            ali_y /= count

            coh_x = (coh_x / count) - self.x
            coh_y = (coh_y / count) - self.y

        # Goal movement
        goal_dx = goal[0] - self.x
        goal_dy = goal[1] - self.y

        # Combine forces
        self.vx += 1.5 * sep_x + 1.0 * ali_x + 1.0 * coh_x + 0.01 * goal_dx
        self.vy += 1.5 * sep_y + 1.0 * ali_y + 1.0 * coh_y + 0.01 * goal_dy

        # Obstacle avoidance
        for obs in obstacles:
            if obs.collidepoint(self.x, self.y):
                self.vx *= -1
                self.vy *= -1

        # Panic mode
        self.max_speed = 3.5 if self.panic else 2

        self.vx, self.vy = limit_vector(self.vx, self.vy, self.max_speed)

        self.x += self.vx
        self.y += self.vy

        # Keep inside screen
        self.x = max(0, min(WIDTH, self.x))
        self.y = max(0, min(HEIGHT, self.y))

    def draw(self, screen):
        color = (255, 255, 0) if self.panic else (0, 255, 0)
        pygame.draw.circle(screen, color, (int(self.x), int(self.y)), 4)

# ---------------- MAIN ----------------
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Smart Crowd Simulator")
clock = pygame.time.Clock()

agents = [Agent(100, 100) for _ in range(NUM_AGENTS)]

goal = (800, 600)

obstacles = [
    pygame.Rect(300, 200, 200, 20),
    pygame.Rect(500, 400, 20, 200)
]

panic_mode = False

running = True
while running:
    screen.fill((0, 0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                panic_mode = not panic_mode
                for a in agents:
                    a.panic = panic_mode

    # Draw goal
    pygame.draw.circle(screen, (0, 0, 255), goal, 8)

    # Draw obstacles
    for obs in obstacles:
        pygame.draw.rect(screen, (255, 0, 0), obs)

    # Update & draw agents
    for agent in agents:
        agent.update(agents, goal, obstacles)
        agent.draw(screen)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
