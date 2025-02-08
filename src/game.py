import sys
from physics import *

pygame.init()

icon = pygame.image.load(WINDOW_ICON_PATH)
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_icon(icon)
pygame.display.set_caption("TurboNafta 3D")
#car_images = [pygame.image.load(os.path.join(CAR_IMAGES_PATH, img)) for img in os.listdir(CAR_IMAGES_PATH)]

clock = pygame.time.Clock()
font = pygame.font.Font('freesansbold.ttf', 32)
text1 = font.render('Player1', True, GRAY)
text2 = font.render('Player2', True, GRAY)

textRect1 = text1.get_rect()
textRect2 = text2.get_rect()
textRect1.center = (100, 50)
textRect2.center = (SCREEN_WIDTH // 2 + 100, 50)

car1 = Car(300, 300, RED, {
    'up': pygame.K_w,
    'down': pygame.K_s,
    'left': pygame.K_a,
    'right': pygame.K_d
})

car2 = Car(850, 300, BLUE, {
    'up': pygame.K_KP8 or pygame.K_UP,
    'down': pygame.K_KP5 or pygame.K_DOWN,
    'left': pygame.K_KP4 or pygame.K_LEFT,
    'right': pygame.K_KP6 or pygame.K_RIGHT
})

track = Track()

# Create cameras
camera1 = Camera(car1.position.x, car1.position.y)
camera2 = Camera(car2.position.x, car2.position.y)

# Create POV's
player1_pov = pygame.Rect(0, 0, SPLIT_WIDTH, SCREEN_HEIGHT)
player2_pov = pygame.Rect(SPLIT_WIDTH, 0, SCREEN_WIDTH, SCREEN_HEIGHT)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    car1.update(track.outer_bounds)
    car2.update(track.outer_bounds)
    car1.check_collision(car2)
    camera1.update(car1.position.x - SPLIT_WIDTH / 2, car1.position.y - SCREEN_HEIGHT / 2)
    camera2.update(car2.position.x - SPLIT_WIDTH / 2, car2.position.y - SCREEN_HEIGHT / 2)

    screen.fill(BLACK)

    track.draw(screen, camera1.position, player1_pov)
    car1.draw(screen, camera1.position, player1_pov)
    car2.draw(screen, camera1.position, player1_pov)

    track.draw(screen, camera2.position, player2_pov)
    car1.draw(screen, camera2.position, player2_pov)
    car2.draw(screen, camera2.position, player2_pov)
    screen.blit(text1, textRect1)
    screen.blit(text2, textRect2)

    pygame.draw.line(screen, BLACK, (SPLIT_WIDTH, 0), (SPLIT_WIDTH, SCREEN_HEIGHT), 2)
    pygame.display.flip()

    clock.tick(FPS)
