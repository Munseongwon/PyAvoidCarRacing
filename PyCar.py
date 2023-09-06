import pygame
import random
from time import sleep

# Game Setting
WINDOW_WIDTH = 480
WINDOW_HEIGHT = 800

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (150, 150, 150)
RED = (255, 0, 0)


# Player and Enemy Class => All of Car class
class Car:
    # Car Image lists
    image_car = ['assets/RacingCar01.png', 'assets/RacingCar02.png', 'assets/RacingCar03.png', 'assets/RacingCar04.png', 'assets/RacingCar05.png', \
                 'assets/RacingCar06.png', 'assets/RacingCar07.png', 'assets/RacingCar08.png', 'assets/RacingCar09.png', 'assets/RacingCar10.png', \
                 'assets/RacingCar11.png', 'assets/RacingCar12.png', 'assets/RacingCar13.png', 'assets/RacingCar14.png', 'assets/RacingCar15.png', \
                 'assets/RacingCar16.png', 'assets/RacingCar17.png', 'assets/RacingCar18.png', 'assets/RacingCar19.png', 'assets/RacingCar20.png']

    # initalizate elements
    def __init__(self, x=0, y=0, dx=0, dy=0):
        self.image = ""
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy

    # car image list loads
    def load_image(self):
        self.image = pygame.image.load(random.choice(self.image_car))
        self.width = self.image.get_rect().size[0]
        self.height = self.image.get_rect().size[1]

    # draw car image lists
    def draw_image(self):
        screen.blit(self.image, [self.x, self.y])

    # move car XAxis moving
    def move_x(self):
        self.x += self.dx

    # move car YAxis moving
    def move_y(self):
        self.y += self.dy

    # Don't split out the playing screen
    def check_out_of_screen(self):
        if self.x + self.width > WINDOW_WIDTH or self.x < 0:
            self.x -= self.dx

    # Player and Enemy crash check
    def check_crash(self, car):
        if (self.x + self.width > car.x) and (self.x < car.x + car.width) and (self.y < car.y + car.height) and (
                self.y + self.height > car.y):
            return True
        else:
            return False


# If you turn on the game screen, first screen's elements are seen
def draw_main_menu():
    draw_x = (WINDOW_WIDTH / 2) - 200
    draw_y = WINDOW_HEIGHT / 2
    image_intro = pygame.image.load('assets/PyCar.png')
    screen.blit(image_intro, [draw_x, draw_y - 200])
    font_40 = pygame.font.SysFont("FixedSys", 40, True, False)
    font_30 = pygame.font.SysFont("FixedSys", 30, True, False)
    text_title = font_40.render("PyCar: Racing Car Game", True, BLACK)
    screen.blit(text_title, [draw_x, draw_y])
    text_score = font_40.render("Score: " + str(score), True, WHITE)
    screen.blit(text_score, [draw_x, draw_y + 70])
    text_start = font_30.render("Press Space Key to Start!", True, RED)
    screen.blit(text_start, [draw_x, draw_y + 140])
    pygame.display.flip()


# Draw the your score
def draw_score():
    font_30 = pygame.font.SysFont("FixedSys", 30, True, False)
    text_score = font_30.render("Score: " + str(score), True, BLACK)
    screen.blit(text_score, [15, 15])


# Start the main system
if __name__ == '__main__':
    pygame.init()

    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("PyCar: Racing Car Game")
    clock = pygame.time.Clock()

    pygame.mixer.music.load('assets/race.wav')
    sound_crash = pygame.mixer.Sound('assets/crash.wav')
    sound_engine = pygame.mixer.Sound('assets/engine.wav')

    player = Car((WINDOW_WIDTH / 2), (WINDOW_HEIGHT - 150), 0, 0)
    player.load_image()

    cars = []
    car_count = 3
    for i in range(car_count):
        x = random.randrange(0, WINDOW_WIDTH - 55)
        y = random.randrange(-150, -50)
        car = Car(x, y, 0, random.randint(5, 10))
        car.load_image()
        cars.append(car)

    lanes = []
    lane_width = 10
    lane_height = 80
    lane_margin = 20
    lane_count = 20
    lane_x = (WINDOW_WIDTH - lane_width) / 2
    lane_y = -10
    for i in range(lane_count):
        lanes.append([lane_x, lane_y])
        lane_y += lane_height + lane_margin

    score = 0
    crash = True
    game_on = True
    while game_on:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_on = False

            if crash:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    crash = False
                    for i in range(car_count):
                        cars[i].x = random.randrange(0, WINDOW_WIDTH - cars[i].width)
                        cars[i].y = random.randrange(-150, -50)
                        cars[i].load_image()

                    player.load_image()
                    player.x = WINDOW_WIDTH / 2
                    player.dx = 0
                    score = 0
                    pygame.mouse.set_visible(False)
                    sound_engine.play()
                    sleep(5)
                    pygame.mixer.music.play(-1)

            if not crash:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        player.dx = 4
                    elif event.key == pygame.K_LEFT:
                        player.dx = -4

                    # add code: Player goes up or down
                    elif event.key == pygame.K_UP:
                        player.dy = -4
                    elif event.key == pygame.K_DOWN:
                        player.dy = 4

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
                        player.dx = 0
                    elif event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                        player.dy = 0

        screen.fill(GRAY)

        if not crash:
            for i in range(lane_count):
                pygame.draw.rect(screen, WHITE, [lanes[i][0], lanes[i][1], lane_width, lane_height])
                lanes[i][1] += 10
                if lanes[i][1] > WINDOW_HEIGHT:
                    lanes[i][1] = -40 - lane_height

            player.draw_image()
            player.move_x()
            player.move_y()  # Player goes up or down
            player.check_out_of_screen()

            for i in range(car_count):
                cars[i].draw_image()
                cars[i].y += cars[i].dy
                if cars[i].y > WINDOW_HEIGHT:
                    score += 10
                    cars[i].x = random.randrange(0, WINDOW_WIDTH - cars[i].width)
                    cars[i].y = random.randrange(-150, -50)
                    cars[i].dy = random.randint(5, 10)
                    cars[i].load_image()

            for i in range(car_count):
                if player.check_crash(cars[i]):
                    crash = True
                    pygame.mixer.music.stop()
                    sound_crash.play()
                    sleep(2)
                    pygame.mouse.set_visible(True)
                    break

            draw_score()
            pygame.display.flip()

        else:
            draw_main_menu()

        clock.tick(60)
