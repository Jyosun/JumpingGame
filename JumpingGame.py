import pygame
import sys
import os
import time

pygame.init()
pygame.display.set_caption('DinoJump')
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 400

current_path = os.path.dirname(__file__)
image_path = os.path.join(current_path, "images") 

# set screen, fps
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
fps = pygame.time.Clock()
 
# dino
dino1 = pygame.image.load(os.path.join(image_path, "dino1.png"))
dino2 = pygame.image.load(os.path.join(image_path, "dino2.png"))
dino_height = dino1.get_size()[1]
dino_bottom = SCREEN_HEIGHT - dino_height
dino_x = 50
dino_y = dino_bottom
jump_top = 200
leg_swap = True
is_go_up = False
 
# tree
tree = pygame.image.load(os.path.join(image_path, "tree.png"))
tree_height = tree.get_size()[1]
tree_x = SCREEN_WIDTH
tree_y = SCREEN_HEIGHT - tree_height
tree_speed = 10
tree_count = 0

pygame.mixer.music.load(os.path.join(image_path, "music.mp3"))
pygame.mixer.music.play(-1)

jumpSound = pygame.mixer.Sound(os.path.join(image_path, "jump.mp3"))
gameOverSound = pygame.mixer.Sound(os.path.join(image_path, "gameover.mp3"))

font = pygame.font.Font(None, 40)

def bad_ending():
    global gameOverSound, screen
    textFont = pygame.font.Font(None, 60)
    text = textFont.render("T_T", True, (0, 0, 0))
    text_pos = text.get_rect()
    text_pos.center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    screen.blit(text, text_pos)
    pygame.display.update()
    pygame.mixer.music.stop()
    gameOverSound.play()
    time.sleep(1)
    pygame.mixer.music.play(-1)

running = True
while running:
    # event check
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                jumpSound.play()
                is_go_up = True

    if is_go_up:
        dino_y -= 10.0
    elif not is_go_up:
        dino_y += 10.0
 
    # dino top and bottom check
    if is_go_up and dino_y <= jump_top:
        is_go_up = False
 
    if dino_y >= dino_bottom:
        is_bottom = True
        dino_y = dino_bottom

    tree_x -= tree_speed
    if tree_x <= 0:
        tree_x = SCREEN_WIDTH
        tree_count += 1
        tree_speed += 0.2
        if tree_speed > 25:
            tree_speed = 25
        
    dino_rect = dino1.get_rect()
    dino_rect.left = dino_x
    dino_rect.top = dino_y
    
    tree_rect = tree.get_rect()
    tree_rect.left = tree_x
    tree_rect.top = tree_y
    
    if dino_rect.colliderect(tree_rect):
        bad_ending()
        running = False
 
    screen.fill((255, 255, 255))

    screen.blit(tree, (tree_x, tree_y))
    
    if leg_swap:
        screen.blit(dino1, (dino_x, dino_y))
        leg_swap = False
    else:
        screen.blit(dino2, (dino_x, dino_y))
        leg_swap = True

    score = font.render("Score:" + str(tree_count), True, (0, 0, 0))
    screen.blit(score, (10, 10))
 
    pygame.display.update()
    fps.tick(30)

pygame.quit()