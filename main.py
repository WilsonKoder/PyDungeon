__author__ = 'WilsonKoder'

# Dungeon Game by Wilson

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ imports

import pygame  # used for graphics
import random  # used for enemy spawning
import sys  # used to close the application
import platform

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

print("Python ", sys.version)
pygame.init()

# Window Setup

windowSize = (800, 600)
window = pygame.display.set_mode(windowSize)

# Clock and FPS

clock = pygame.time.Clock()
FPS_LIMIT = 60

# Game Variables

colors = {"red": (255, 0, 0), "green": (0, 255, 0), "blue": (0, 0, 255), "white": (255, 255, 255), "black": (0, 0, 0),
          "yellow": (255, 255, 0)}

running = True

# Fonts

defaultFont = pygame.font.SysFont(None, 48)

# BG

bg = pygame.image.load("res/img/background-image.png")

# Input

moveUp = False
moveDown = False
moveLeft = False
moveRight = False

# Player Variables

playerPosition = [400, 300]
PLAYER_IMG_PATH = "res/img/player.png"
playerImage = pygame.image.load(PLAYER_IMG_PATH)
playerSpeed = 5
playerScore = 0
playerAmmo = 100
dead = False
scores = ""
loadScores = False
showText = False

# Projectile Class

projectiles = []
PROJECTILE_IMG_PATH = "res/img/projectile.png"
projectileImage = pygame.image.load(PROJECTILE_IMG_PATH)

class Projectile:

    direction = ""
    pos = [1, 1]

    def __init__(self, dir, playerPos):
        if dir is "up" or "down" or "left" or "right":

            self.direction = dir
            self.pos = [playerPos[0] - 14, playerPos[1] - 14]  # add an offset to makesure that the bullets line up with the player

    def update_pos(self):
        if self.direction is "up":
            self.pos[1] -= 10
        elif self.direction is "down":
            self.pos[1] += 10
        elif self.direction is "left":
            self.pos[0] -= 10
        elif self.direction is "right":
            self.pos[0] += 10

# Enemy class

enemies = []
count = 0
enemySpeed = 3


class Enemy:
    pos = [1, 1]

    def __init__(self):
        self.pos = [random.randint(0, 799), random.randint(0, 599)]

    def match_position(self, player_pos):
        if self.pos[0] < player_pos[0]:
            self.pos[0] += enemySpeed
        else:
            self.pos[0] -= enemySpeed

        if self.pos[1] < player_pos[1]:
            self.pos[1] += enemySpeed
        else:
            self.pos[1] -= enemySpeed


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ functions

def draw_enemies():
    for enemy in enemies:
        pygame.draw.circle(window, colors["green"], enemy.pos, 14, 0)


def draw_projectiles():
    for projectile in projectiles:
        position = projectile.pos
        window.blit(projectileImage, position)


def clean_memory():
    for proj in projectiles:
        if proj.pos[0] > 800 or proj.pos[0] < -14 or proj.pos[1] < -14 or proj.pos[1] > 814:
            projectiles.remove(proj)

# collision algorthim taken from https://developer.mozilla.org/en-US/docs/Games/Techniques/2D_collision_detection


def check_projectile_collision():
    for enemy in enemies:
        for proj in projectiles:
            if enemy.pos[0] < proj.pos[0] + 28 and enemy.pos[0] + 28 > proj.pos[0] and enemy.pos[1] < proj.pos[1] + 14 and enemy.pos[1] + 14 > proj.pos[1]:
                print("shot")
                try:
                    enemies.remove(enemy)
                    projectiles.remove(proj)
                except ValueError:
                    print("oops!")
                return True


def check_player_collision():
    for enemy in enemies:
        if enemy.pos[0] < playerPosition[0] + 28 and enemy.pos[0] + 28 > playerPosition[0] and enemy.pos[1] < playerPosition[1] + 14 and enemy.pos[1] + 14 > playerPosition[1]:
            return True

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Main loop

while running:
    clock.tick(FPS_LIMIT)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            # movement
            if event.key == pygame.K_w:
                moveUp = True
            elif event.key == pygame.K_s:
                moveDown = True

            if event.key == pygame.K_a:
                moveLeft = True
            elif event.key == pygame.K_d:
                moveRight = True

            if event.key == pygame.K_p:
                playerSpeed = 10

            # shooting

            if event.key == pygame.K_UP:
                if playerAmmo > 0:
                    playerAmmo -= 1
                    proj = Projectile("up", playerPosition)
                    projectiles.append(proj)

            elif event.key == pygame.K_DOWN:
                if playerAmmo > 0:
                    playerAmmo -= 1
                    proj = Projectile("down", playerPosition)
                    projectiles.append(proj)

            if event.key == pygame.K_LEFT:
                if playerAmmo > 0:
                    playerAmmo -= 1
                    proj = Projectile("left", playerPosition)
                    projectiles.append(proj)

            elif event.key == pygame.K_RIGHT:
                if playerAmmo > 0:
                    playerAmmo -= 1
                    proj = Projectile("right", playerPosition)
                    projectiles.append(proj)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_w:
                moveUp = False
            elif event.key == pygame.K_s:
                moveDown = False

            if event.key == pygame.K_a:
                moveLeft = False
            elif event.key == pygame.K_d:
                moveRight = False

    for projectile in projectiles:
        projectile.update_pos()

    if moveUp:
        playerPosition[1] -= playerSpeed
    elif moveDown:
        playerPosition[1] += playerSpeed

    if moveLeft:
        playerPosition[0] -= playerSpeed
    elif moveRight:
        playerPosition[0] += playerSpeed

    if playerPosition[0] > 815:
        playerPosition[0] = -15
    elif playerPosition[0] < -15:
        playerPosition[0] = 815

    if playerPosition[1] > 615:
        playerPosition[1] = -15
    elif playerPosition[1] < -15:
        playerPosition[1] = 615

    count += 1

    if count > 50:
        new_enemy = Enemy()
        enemies.append(new_enemy)
        count = 0

    for enemy in enemies:
        enemy.match_position(playerPosition)

    shot = check_projectile_collision()
    if shot:
        playerScore += 1
        playerAmmo += 2

    playerStatus = check_player_collision()

    if playerStatus:
        dead = True
        loadScores = True

    window.fill(colors["yellow"])

    window.blit(bg, (0, 0))

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ drawing code under here

    if not dead:
        scoreText = defaultFont.render(str(playerScore), 1, colors["red"])
        ammoText  = defaultFont.render("Ammo: " + str(playerAmmo), 1, colors["red"])

        draw_projectiles()
        draw_enemies()
        window.blit(playerImage, (playerPosition[0] - 14, playerPosition[1] - 14))
        window.blit(scoreText, (380, 20))
        window.blit(ammoText, (600, 20))
        clean_memory()
    else:
        if showText:
            scoreList = scores.split("|")
            scoreList.remove('')  # this will throw an error when we try to convert the list to an integer list if we don't do it
            for score in scoreList:
                score = int(score)
            scoreList.sort()
            scoreList.reverse()  # sort() gives us a reversed one, so reverse it again.
            ypos = 20

            title = defaultFont.render("High Scores: ", 1, colors["red"])
            window.blit(title, (300, 0))

            for score in scoreList:
                ypos += 30
                scoresText = defaultFont.render(str(score), 1, colors["red"])
                window.blit(scoresText, (380, ypos))

        elif loadScores:
            try:
                scoreFile = open("pScores.su", "a")
                if playerScore is not 0:
                    scoreFile.write(str(playerScore) + "|")
                scoreFile.close()
                scoreFile = open("pScores.su", "r")
                scores = scoreFile.readline()
                showText = True
            except FileNotFoundError:
                scoreFile = open("pScores.su", "x")
                if playerScore is not 0:
                    scoreFile.write(str(playerScore) + "|")
                scoreFile.close()
                scoreFile = open("pScores.su", "r")
                scores = scoreFile.readline()
                showText = True

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    pygame.display.flip()

pygame.quit()
sys.exit()

# ~~~~~~~~~~~ 312 Lines ~~~~~~~~~~~~