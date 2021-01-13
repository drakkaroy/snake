import pygame
import random


def rand_position(rows, cols):
    r = random.randint(0, rows - 1)
    c = random.randint(0, cols - 1)
    return r, c


def rand_target(rows, cols, exclude):
    while True:
        target = rand_position(rows, cols)
        if target not in exclude:
            return target


def clip(r, c, rows, cols):
    if c < 0:
        c += cols
    elif c >= cols:
        c -= cols

    if r < 0:
        r += rows
    elif r >= rows:
        r -= rows

    return r, c


def draw_block(screen, position, block_size, color):
    r, c = position
    r *= block_size
    c *= block_size
    pygame.draw.rect(screen, color, (c + 1, r + 2, block_size - 2, block_size - 2))


def draw_target(screen, target, block_size):
    color = (20, 100, 200)
    draw_block(screen, target, block_size, color)


def out_of_bounds(rows, cols, pos):
    r, c = pos
    if r < 0 or r >= rows:
        return True
    if c < 0 or c >= cols:
        return True
    return False


def opposing(a, b):
    if a > b:
        a, b = b, a
    if [a, b] == [0, 2]:
        return True
    elif [a, b] == [1, 3]:
        return True
    return False


class Snake:

    def __init__(self, block_size):
        w, h = pygame.display.get_surface().get_size()
        self.rows = h // block_size
        self.cols = w // block_size
        self.positions = [(self.rows // 2, self.cols // 2), ]
        self.direction = random.randint(0, 3)

        self.font = pygame.font.SysFont("arial", 16)

    def self_intersect(self):
        return self.positions[0] in self.positions[1:]

    def move(self, pos):
        r, c = pos
        if self.direction == 0:
            c -= 1
        elif self.direction == 1:
            r -= 1
        elif self.direction == 2:
            c += 1
        elif self.direction == 3:
            r += 1
        return clip(r, c, self.rows, self.cols)

    def step(self, game_over):
        if not game_over:
            r, c = self.positions[0]
            self.positions.pop()
            self.positions.insert(0, self.move((r, c)))

    def draw(self, screen):
        colors = [(40, 40, 40), (90, 90, 90)]
        for k, position in enumerate(self.positions):
            draw_block(screen, position, block_size, colors[k % 2])

    def draw_score(self, screen):
        score = len(self.positions) - 1
        score_surface = self.font.render("Score: " + str(score), True, (250, 150, 250), (30, 30, 30))
        screen.blit(source=score_surface, dest=(10, 10))


def run(w, h, block_size):
    pygame.init()
    assert pygame.get_init()

    screen = pygame.display.set_mode((w, h))

    done = False
    backgroundColor = (170, 160, 50)
    clock = pygame.time.Clock()

    s = Snake(block_size)
    target = rand_target(w // block_size, h // block_size, s.positions)

    game_over = False
    fps = 10

    # Remove initial events from queue
    for e in pygame.event.get():
        pass

    while not done:

        new_dir = s.direction

        event = pygame.event.poll()
        if event.type == pygame.QUIT:
            done = True
        elif not game_over:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    new_dir = 0
                elif event.key == pygame.K_UP:
                    new_dir = 1
                elif event.key == pygame.K_RIGHT:
                    new_dir = 2
                elif event.key == pygame.K_DOWN:
                    new_dir = 3

            if not opposing(s.direction, new_dir):
                s.direction = new_dir
                s.step(game_over)

            if target == s.positions[0]:
                s.positions.append(s.positions[-1])
                target = rand_target(w // block_size, h // block_size, s.positions)
                fps *= 1.02
            elif s.self_intersect():
                game_over = True

        screen.fill(backgroundColor)
        draw_target(screen, target, block_size)
        s.draw(screen)
        s.draw_score(screen)
        pygame.display.flip()

        clock.tick(fps)


if __name__ == "__main__":
    block_size = 15
    width = block_size * 30
    height = block_size * 30
    run(width, height, block_size)
