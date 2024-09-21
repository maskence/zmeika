import pygame as pg
import time
import random
import json 
from datetime import datetime

def render_centered_text(text, font_name, surface, size=10, color = (239, 239, 42), x=0, y=0, horizontally = True, vertically = False):
    font = pg.font.SysFont(font_name, size)
    text_w, text_h = font.size(text)
    if horizontally:
        x = surface.get_width() // 2 - text_w // 2 
    if vertically:
        y = surface.get_height() // 2 - text_h // 2
    text_surface = font.render(text, True, color)
    screen.blit(text_surface,(x,y))

# pygame setup
pg.init()
screen_w, screen_h = 720,720
screen = pg.display.set_mode((screen_w, screen_w))
clock = pg.time.Clock()
running = True
pg.display.set_caption('Zmeika')
icon = pg.image.load('snake_head.png')
pg.display.set_icon(icon)

# game setup
grid_w, grid_h = 8,8
tile_h, tile_w = screen_h // grid_h, screen_w // grid_w
snake = [(3,3, pg.K_RIGHT),(4,3, pg.K_RIGHT)]
apples = [(6,6)]
speed_x, speed_y = 1,0
last_direction_pressed = pg.K_RIGHT
score = 2
date = datetime.today().strftime('%d/%m/%Y')
game_over = False

with open("high_scores.json", 'r') as f:
    high_scores = json.load(f)


if date[:-5] == "30/05":
    apple_sprite = pg.image.load('cake.png').convert_alpha() 
    snake_head = pg.image.load('birthday_snake_head.png').convert_alpha()
else:
    apple_sprite = pg.image.load('apple.png').convert_alpha()
    snake_head = pg.image.load('snake_head.png').convert_alpha()

snake_head = pg.transform.scale(snake_head,(tile_w, tile_h))
apple_sprite = pg.transform.scale(apple_sprite,(tile_w, tile_h))

snake_body = pg.image.load('snake_body.png').convert_alpha()
snake_body = pg.transform.scale(snake_body,(tile_w, tile_h))

snake_tail = pg.image.load('snake_tail.png').convert_alpha()
snake_tail = pg.transform.scale(snake_tail,(tile_w, tile_h))


direction_to_angle = { pg.K_UP : 90, pg.K_DOWN : 270, pg.K_LEFT : 180, pg.K_RIGHT : 0}

last_input_time = pg.time.get_ticks()
while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        if event.type == pg.KEYDOWN:
            if event.key in (pg.K_LEFT, pg.K_RIGHT, pg.K_UP, pg.K_DOWN):
                last_direction_pressed = event.key


    ##UPDATE STATE
    current_time = pg.time.get_ticks()
    if  current_time - last_input_time > 500:
        if last_direction_pressed == pg.K_UP and speed_y != 1:
            speed_x, speed_y = 0, -1
        elif last_direction_pressed == pg.K_DOWN and speed_y != -1:
            speed_x, speed_y = 0, 1
        elif last_direction_pressed == pg.K_LEFT and speed_x != 1:
            speed_x, speed_y = -1, 0
        elif last_direction_pressed == pg.K_RIGHT and speed_x != -1:
            speed_x, speed_y = 1, 0

        new_segment = (snake[-1][0] + speed_x, snake[-1][1] + speed_y, last_direction_pressed)

        if new_segment[:2] in apples:
            apples.remove(new_segment[:2])

            new_apple = (random.randint(0, grid_h -1), random.randint(0, grid_w -1))
            while new_apple in (segment[:2] for segment in snake):
                print('apple fell in snake, trying with new one')
                new_apple = (random.randint(0, grid_h -1), random.randint(0, grid_w -1))
            apples.append(new_apple)
        else:
            snake.pop(0)

        if new_segment[1] not in range(0,grid_h) or new_segment[0] not in range(0,grid_w) or new_segment[:2] in (segment[:2] for segment in snake):
            game_over = True
        snake.append(new_segment)
        last_input_time = current_time

    ## RENDER
    screen.fill("purple")
    #draw grid
    for i in range(grid_h + 1):
        pg.draw.line(screen, color = (0,0,0,), start_pos=(0,tile_h * i), end_pos = (screen_w, tile_h * i), width = 0)
    for i in range(grid_w + 1):
        pg.draw.line(screen, color = (0,0,0,), start_pos=(tile_w * i, 0), end_pos = (tile_w * i, screen_h), width = 0)
    
    #draw snake 
    for x,y, direction in snake[1:-1]:
        rotation_angle = direction_to_angle[direction]
        screen.blit(pg.transform.rotate(snake_body,rotation_angle), (x * tile_w, y * tile_h))
    
    tail = snake[0]
    rotation_angle = direction_to_angle[snake[1][2]] 
    screen.blit(pg.transform.rotate(snake_tail,rotation_angle), (tail[0] * tile_w, tail[1] * tile_h))

    head = snake[-1]
    rotation_angle = direction_to_angle[head[2]] 
    screen.blit(pg.transform.rotate(snake_head,rotation_angle), (head[0] * tile_w, head[1] * tile_h))

    #draw apples
    for x,y in apples:
        screen.blit(apple_sprite, (x * tile_w, y * tile_h))

    pg.display.flip()
    if game_over:
        score = len(snake)
        high_scores.append({"date":date, "score": score})
        high_scores.sort(key= lambda x : -x['score'])
        high_scores = high_scores[:3]

        with open('high_scores.json', 'w') as f:
            json.dump(high_scores,f)
        break
    clock.tick(60)  

while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    render_centered_text("GAME OVER!", 'arial', screen, y=100, size = 90)
    render_centered_text(f" Score : {score}", 'arial', screen, y=200, size=50)

    render_centered_text(f" Highscores :", 'arial', screen, y=300, size=50)
    for i,high_score in enumerate(high_scores):
        render_centered_text(f"{high_score['date']} : {high_score['score']}", 'arial', screen, y=400 + i * 100, size = 40)

    pg.display.flip()
    clock.tick(10)

pg.quit()