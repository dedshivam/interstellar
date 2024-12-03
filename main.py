import pygame
import random
import math
from pygame import mixer

pygame.init()
screen = pygame.display.set_mode((800,650))
pygame.display.set_caption(". "+"Ｉｎｔｅｒｓｔｅｌｌａｒ")
background_img = pygame.image.load("backgroundd.png")
icon = pygame.image.load("startup.png")
pygame.display.set_icon(icon)



#player
player_img = pygame.image.load("spaceship.png")
playerX = 368
playerY = 550
playerX_chng = 0

# many enemies...
enemy_img =[]
enemyX = []
enemyY =[]
enemyX_chng =[]
enemyY_chng =[]
num_of_enemies = 6

#enemy1
for i in range(num_of_enemies):
    enemy_img.append(pygame.image.load("art.png"))
    enemyX.append(random.randint(0,735))
    enemyY.append(random.randint(0,150))
    enemyX_chng.append(0.3)
    enemyY_chng.append(30)
mixer.music.load('background.wav')
mixer.music.play(-1)

#bullet
bullet_img = pygame.image.load("bullet.png")
bulletX = 0
bulletY = 550
bulletX_chng = 0
bulletY_chng = 0.8
bullet_state = "ready"

#score
score_value = 0
font = pygame.font.Font('font1.ttf',32)
textX = 10
textY = 10
over_font = pygame.font.Font('font1.ttf',54)
def game_over_text():
    over_text = over_font.render("Game Over!!",True,(255,255,255))
    screen.blit(over_text,(180,195))
def show_score(x,y):
    score = font.render("Score :"+ str(score_value),True,(255,255,255))
    screen.blit(score,(x,y))
def player(x,y):
    screen.blit(player_img,(x,y))
def enemy(x,y,i):
    screen.blit(enemy_img[i],(x,y))  
def bullet(x,y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bullet_img,(x+16,y+10))
def iscollision(enemyX,enemyY,bulletX,bulletY):
    distance = math.sqrt((math.pow(enemyX-bulletX,2))+math.pow(enemyY-bulletY,2))
    if distance < 27:
        return True
    else:
        return False 
    
running = True
while running:
    screen.fill((20,20,20))
    screen.blit(background_img,(0,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False    
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_chng = -0.5
            elif event.key == pygame.K_RIGHT:
                playerX_chng = 0.5 
            elif event.key == pygame.K_SPACE:
                if bullet_state is "ready":
                    bullet_sound = mixer.Sound('laser.wav')
                    bullet_sound.play()
                    bulletX = playerX
                    bullet(bulletX,bulletY)            
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_chng =0
                
    playerX += playerX_chng
    if playerX <=4:
        playerX = 4
    if playerX >=732:
        playerX = 732   
    for i in range(num_of_enemies):  
        if enemyY[i]  >250:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break
        enemyX[i] += enemyX_chng[i]
        if enemyX[i] <=4:
            enemyX_chng[i] = 0.3
            enemyY[i] = enemyY[i] + enemyY_chng[i]
        if enemyX[i] >=732:
            enemyY[i] = enemyY[i] + enemyY_chng[i]
            enemyX_chng[i] = -0.3
        collision = iscollision(enemyX[i],enemyY[i],bulletX,bulletY)
        if collision:
            col_sound = mixer.Sound('explosion.wav')
            col_sound.play()
            bulletY = 550
            bullet_state = "ready"
            score_value +=1
            print(score_value)
            enemyX[i] = random.randint(0,735)
            enemyY[i] = random.randint(0,150) 
        enemy(enemyX[i],enemyY[i],i)
    if bulletY<=-20:
        bulletY = 550
        bullet_state = "ready"
    if bullet_state is "fire":
        bullet(bulletX,bulletY)
        bulletY -= bulletY_chng
    player(playerX,playerY) 
    show_score(textX,textY)
    pygame.display.update()        
