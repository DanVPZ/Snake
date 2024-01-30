import os
import random
import sys
import time

import pygame

# Screen Settings
pygame.init()
clock = pygame.time.Clock()
screen_width = 800
screen_height = 800
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Snake Game")
columns = 20
rows = 20
cell_size = screen_width / columns
rotate = False
angle = 90
directory = os.getcwd()

images = [
    pygame.image.load(".\\img\\head1.png").convert_alpha(),
    pygame.image.load(".\\img\\head2.png").convert_alpha(),
    pygame.image.load(".\\img\\head3.png").convert_alpha(),
    pygame.image.load(".\\img\\tail.png").convert_alpha(),
    pygame.image.load(".\\img\\fruit.png").convert_alpha(),
    pygame.image.load(".\\img\\corner3.png").convert_alpha(),
]


# Kills the process
def end_game():
    screen.fill(border_color)
    screen.blit(loser_text, (screen_width / 2 - 195, screen_height / 2 - 65))
    pygame.display.update()
    clock.tick(10)
    time.sleep(5)
    sys.exit()

# Dibuja la cuadrícula
def draw_grid():
    for row in range(rows):
        for col in range(columns):
            pygame.draw.rect(screen, black, (col * cell_size, row * cell_size, cell_size, cell_size), 1)

            if row == rows - 1 or col == columns - 1 or row == 0 or col == 0:
                pygame.draw.rect(screen, border_color, (col * cell_size, row * cell_size, cell_size, cell_size))

def draw_fruit():
    global fruit, fruit_x, fruit_y, fruit_sprite, fruit_surface
    if fruit == True:
        return

    fruit_x = random.randint(1, rows - 2)
    fruit_y = random.randint(1, columns - 2)
    
    fruit = True

# All game-ending collisions
def gameEnd_collisions():
    if x_pos * cell_size < cell_size or x_pos * cell_size > screen_width - cell_size * 1.8:
        end_game()
        print("x fuera")
    elif y_pos * cell_size < cell_size or y_pos * cell_size > screen_height - cell_size * 1.8:
        end_game()
        print("y fuera")

def fruit_collisions():
    global fruit_x, fruit_y, tail_size, fruit
    if fruit_x == x_pos:
        if fruit_y == y_pos:
            tail_size += 1
            fruit = False

def draw_snake():
    global rotate, angle
    # Draws Head
    head_surface = pygame.Surface([cell_size, cell_size], pygame.SRCALPHA)
    head_surface.blit(images[0], (0, 0))
    head_sprite = pygame.transform.scale(head_surface, (cell_size, cell_size))

    if direc == "left":
        head_sprite = pygame.transform.rotate(head_sprite, -90)
    elif direc == "right":
        head_sprite = pygame.transform.rotate(head_sprite, 90)
    elif direc == "up":
        head_sprite = pygame.transform.rotate(head_sprite, 180)
    elif direc == "down":
        pass

    screen.blit(head_sprite, (x_pos * cell_size, y_pos * cell_size))

    # Draws Tail

    a = 0

    for pos in tail_pos:

        if tail_direc[a + 1] != tail_direc[a]:

            img_pos = 5
        
            if tail_direc[a+1] == "left" and tail_direc[a] == "up" or tail_direc[a+1] == "down" and tail_direc[a] == "right":
                rotate = True
                angle = 0
            elif tail_direc[a+1] == "up" and tail_direc[a] == "right" or tail_direc[a+1] == "left" and tail_direc[a] == "down":
                rotate = True
                angle = -90
            elif tail_direc[a+1] == "up" and tail_direc[a] == "left" or tail_direc[a+1] == "right" and tail_direc[a] == "down":
                rotate = True
                angle = 180
            elif tail_direc[a+1] == "right" and tail_direc[a] == "up" or tail_direc[a+1] == "down" and tail_direc[a] == "left":
                rotate = True
                angle = 90

        else:

            img_pos = 3
            angle = 90

            if tail_direc[a] == "left":
                rotate = True
            elif tail_direc[a] == "right":
                rotate = True
            elif tail_direc[a] == "up":
                rotate = True
                angle = 0
            elif tail_direc[a] == "down":
                rotate = True
                angle = 0

        a += 1

        tail_surface = pygame.Surface([cell_size, cell_size], pygame.SRCALPHA)
        tail_surface.blit(images[img_pos], (0, 0))
        tail_sprite = pygame.transform.scale(tail_surface, (cell_size, cell_size))

        if rotate:
            tail_sprite = pygame.transform.rotate(tail_sprite, angle)
        
        screen.blit(tail_sprite, (pos[0] * cell_size, pos[1] * cell_size))


def movement():
    global x_pos, y_pos, direc, tail_pos, tail_size, fruit_x, fruit_y, tail_direc

    # Agrega la posición actual de la cabeza de la serpiente al principio de la lista de tail_pos.
    tail_pos.insert(0, (x_pos, y_pos))
    tail_direc.insert(0, direc)

    # Limita la longitud de tail_pos al tamaño de la cola deseado.
    tail_pos = tail_pos[:tail_size]
    tail_direc = tail_direc[:tail_size + 1]
    
    # Actualiza la posición de la cabeza de la serpiente.
    if direc == "left":
        x_pos -= 1
    elif direc == "right":
        x_pos += 1
    elif direc == "up":
        y_pos -= 1
    elif direc == "down":
        y_pos += 1

    # Actualiza la pantalla.
    pygame.display.update()


grid = []
for row in range(rows):
    grid.append([])
    for column in range(columns):
        grid[row].append(0)

x_pos = random.randint(0, rows - 2)
y_pos = random.randint(0, columns - 2)
fruit_x = 0
fruit_y = 0
direc = ""
tail = []
tail_pos = []
tail_direc = ["right"]
corner_pos = []
tail_size = 1
x_tail = 0
y_tail = 0

fruit = False
fruit_surface = pygame.Surface([cell_size, cell_size], pygame.SRCALPHA)
fruit_surface.blit(images[4], (0, 0))
fruit_sprite = pygame.transform.scale(fruit_surface, (cell_size, cell_size))

# Colors
back_color = pygame.Color('palegreen4')
white = 255, 255, 255
black = 0, 0, 0
border_color = pygame.Color("grey12")
head_color = 200, 10 , 10
tail_color = 10, 200, 10
fruit_color = 10, 10, 200

freesans_bold = pygame.font.Font('freesansbold.ttf', 80)
loser_text = freesans_bold.render("Game Over", True, white)

# Main Loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        
        elif event.type == pygame.KEYDOWN:

            if event.key == pygame.K_a and direc != "right":
                direc = "left"
            elif event.key == pygame.K_d and direc != "left":
                direc = "right"
                
            elif event.key == pygame.K_w and direc != "down":
                direc = "up"
            elif event.key == pygame.K_s and direc != "up":
                direc = "down"
                
        x_head = x_tail * cell_size
        y_head = y_tail * cell_size
            
    
    screen.fill(back_color)
    draw_grid()

    draw_fruit()
    screen.blit(fruit_sprite, (fruit_x * cell_size, fruit_y * cell_size))
    
    movement()
    
    fruit_collisions()
    draw_snake()

    print(tail_direc)

    gameEnd_collisions()
    pygame.display.flip()
    clock.tick(5)
