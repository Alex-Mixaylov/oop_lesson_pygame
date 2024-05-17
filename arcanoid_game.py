import pygame
import sys

# Инициализация Pygame
pygame.init()

# Цвета
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)

# Основные параметры окна
SCREEN_WIDTH, SCREEN_HEIGHT = 600, 400
FPS = 60

class Paddle:
    def __init__(self):
        self.width = 100
        self.height = 10
        self.x = (SCREEN_WIDTH - self.width) // 2
        self.y = SCREEN_HEIGHT - self.height - 20
        self.speed = 6

    def move(self, keys):
        if keys[pygame.K_LEFT] and self.x > 0:
            self.x -= self.speed
        if keys[pygame.K_RIGHT] and self.x < SCREEN_WIDTH - self.width:
            self.x += self.speed

    def draw(self, screen):
        pygame.draw.rect(screen, WHITE, (self.x, self.y, self.width, self.height))

class Ball:
    def __init__(self, paddle):
        self.radius = 8
        self.paddle = paddle
        self.reset()

    def move(self):
        self.x += self.speed_x
        self.y += self.speed_y

    def bounce(self):
        if self.x <= 0 or self.x >= SCREEN_WIDTH:
            self.speed_x = -self.speed_x
        if self.y <= 0:
            self.speed_y = -self.speed_y
        if self.y >= SCREEN_HEIGHT:
            self.reset()

    def reset(self):
        self.x = SCREEN_WIDTH // 2
        self.y = self.paddle.y - self.radius
        self.speed_x = 4
        self.speed_y = -4

    def draw(self, screen):
        pygame.draw.circle(screen, BLUE, (self.x, self.y), self.radius)

class Brick:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)

    def draw(self, screen):
        pygame.draw.rect(screen, WHITE, self.rect)

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Арканоид")
        self.clock = pygame.time.Clock()
        self.paddle = Paddle()
        self.ball = Ball(self.paddle)
        self.bricks = self.create_bricks()

    def create_bricks(self):
        bricks = []
        brick_rows = 5
        brick_cols = 10
        brick_width = SCREEN_WIDTH // brick_cols
        brick_height = 20
        brick_gap = 5

        for row in range(brick_rows):
            for col in range(brick_cols):
                x = col * (brick_width + brick_gap)
                y = row * (brick_height + brick_gap)
                bricks.append(Brick(x, y, brick_width, brick_height))

        return bricks

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            keys = pygame.key.get_pressed()
            self.paddle.move(keys)
            self.ball.move()
            self.ball.bounce()

            # Столкновение с платформой
            if (self.paddle.x <= self.ball.x <= self.paddle.x + self.paddle.width and
                    self.paddle.y <= self.ball.y + self.ball.radius <= self.paddle.y + self.paddle.height):
                self.ball.speed_y = -self.ball.speed_y

            # Столкновение с кирпичами
            for brick in self.bricks:
                if brick.rect.collidepoint(self.ball.x, self.ball.y):
                    self.bricks.remove(brick)
                    self.ball.speed_y = -self.ball.speed_y
                    break

            # Очистка экрана
            self.screen.fill(BLACK)

            # Рисование объектов
            self.paddle.draw(self.screen)
            self.ball.draw(self.screen)
            for brick in self.bricks:
                brick.draw(self.screen)

            # Обновление экрана
            pygame.display.flip()

            # Контроль ФПС
            self.clock.tick(FPS)

        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game()
    game.run()
