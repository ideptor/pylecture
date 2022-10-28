import pygame
import random
from time import sleep


BLACK = (0,0,0)
WHITE = (255,255,255)
RED=(255,0,0)
pad_width=480
pad_height=840
fight_width=36
fight_height=38
enemy_width=26
enemy_height=20

END_ENEMY_PASSED = 3
ENEMY_SPEED_LIMIT = 10
BULLET_LIMIT = 5

def drawScore(count):
    global gamepad
    font = pygame.font.SysFont(None, 20)
    text = font.render("Enemy Kills: " + str(count), True, WHITE)
    gamepad.blit(text, (0,0))


def drawPassed(count):
    global gamepad
    font = pygame.font.SysFont(None, 20)
    text = font.render("Enemy Passed: " + str(count), True, RED)
    gamepad.blit(text, (360,0))


def dispMessage(text):
    global gamepad
    # textfont = pygame.font.Font("freescansbold.ttf", 20)
    textfont = pygame.font.SysFont(None, 20)
    text = textfont.render(text, True, RED)
    textpos = text.get_rect()
    textpos.center = (pad_width/2, pad_height/2)
    gamepad.blit(text, textpos)
    pygame.display.update()
    sleep(2)
    runGame()


def crash():
    global gamepad
    dispMessage("Crashed!")    


def gameover():
    global gamepad
    dispMessage("Game Over")    


def drawObject(obj, x, y):
    global gamepad
    gamepad.blit(obj, (x,y))


def runGame():
    global gamepad, clock, fighter, enemy, bullet

    isShot = False
    shotcount = 0
    enemypassed = 0

    bullet_xy = []

    x = pad_width*0.45
    y = pad_height*0.9
    x_change = 0

    enemy_x = random.randrange(0, pad_width - enemy_width)
    enemy_y = 0
    enemy_speed = 3

    ongame = False
    while not ongame:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                ongame = True

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_LEFT:
                    x_change -= 5

                elif event.key == pygame.K_RIGHT:
                    x_change += 5                
                        
                elif event.key == pygame.K_LCTRL:
                    if len(bullet_xy) < BULLET_LIMIT:
                        bullet_x = x + fight_width/2
                        bullet_y = y - fight_height
                        bullet_xy.append([bullet_x, bullet_y])

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    x_change = 0

        gamepad.fill(BLACK)

        x += x_change
        if x < 0:
            x = 0
        elif x > pad_width - fight_width:
            x = pad_width - fight_width

        if y < enemy_y + enemy_height:
            if (enemy_x > x and enemy_x < x + fight_width) or \
                (enemy_x + enemy_width > x and enemy_x + enemy_width < x + fight_width):
                crash()

        drawObject(fighter, x, y)

        if len(bullet_xy) != 0:
            for i, bxy in enumerate(bullet_xy):
                bxy[1] -= 10
                bullet_xy[i][1] = bxy[1]  # simplify???

            if bxy[1] < enemy_y:
                if bxy[0] > enemy_x and bxy[0] < enemy_x + enemy_width:
                    bullet_xy.remove(bxy)
                    isShot = True
                    shotcount += 1

            if bxy[1] <= 0:
                try:
                    bullet_xy.remove(bxy)
                except:
                    print("exception on remove bullet")

        if len(bullet_xy) != 0:
            for bx, by in bullet_xy:
                drawObject(bullet, bx, by)

        drawScore(shotcount)

        enemy_y += enemy_speed
        enemy_x_change = random.randrange(-2, 2)
        enemy_x += enemy_x_change
        enemy_x = max(0, enemy_x)
        enemy_x = min(pad_width-enemy_width, enemy_x)

        if enemy_y > pad_height:
            enemy_y = 0
            enemy_x = random.randrange(0, pad_width-enemy_width)
            enemypassed += 1

        if enemypassed == END_ENEMY_PASSED:
            gameover()

        drawPassed(enemypassed)

        if isShot:
            enemy_speed = min(ENEMY_SPEED_LIMIT, enemy_speed + 1)
            enemy_y=0
            enemy_x = random.randrange(0, pad_width-enemy_width)
            isShot = False
    
        drawObject(enemy, enemy_x, enemy_y)

        pygame.display.update()
        clock.tick(60)

    pygame.quit()


def initGame():
    global gamepad, clock, fighter, enemy, bullet

    pygame.init()
    gamepad = pygame.display.set_mode((pad_width, pad_height))
    pygame.display.set_caption("Invader")
    fighter = pygame.image.load("fighter.png")
    enemy = pygame.image.load("enemy.png")
    bullet = pygame.image.load("bullet.png")
    clock = pygame.time.Clock()

initGame()
runGame()
        