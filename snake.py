# Simple Snake Game using pygame – a tiny, whimsical implementation
import pygame, sys, random

pygame.init()
WIDTH, HEIGHT = 640, 480
CELL_SIZE = 20
cols, rows = WIDTH // CELL_SIZE, HEIGHT // CELL_SIZE
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

BLACK = (0,0,0)
GREEN = (0,255,0)
RED = (255,0,0)
WHITE = (255,255,255)

snake = [(cols//2, rows//2)]
direction = (0,-1)
food = (random.randint(0, cols-1), random.randint(0, rows-1))
font = pygame.font.SysFont(None,24)

def draw_cell(pos,color):
    x,y=pos
    rect=pygame.Rect(x*CELL_SIZE,y*CELL_SIZE,CELL_SIZE,CELL_SIZE)
    pygame.draw.rect(screen,color,rect)

while True:
    for e in pygame.event.get():
        if e.type==pygame.QUIT:
            pygame.quit();sys.exit()
        elif e.type==pygame.KEYDOWN:
            if e.key==pygame.K_UP and direction!=(0,1): direction=(0,-1)
            elif e.key==pygame.K_DOWN and direction!=(0,-1): direction=(0,1)
            elif e.key==pygame.K_LEFT and direction!=(1,0): direction=(-1,0)
            elif e.key==pygame.K_RIGHT and direction!=(-1,0): direction=(1,0)
    head=(snake[0][0]+direction[0], snake[0][1]+direction[1])
    head=(head[0]%cols, head[1]%rows)
    snake.insert(0,head)
    if head==food:
        while True:
            food=(random.randint(0,cols-1),random.randint(0,rows-1))
            if food not in snake: break
    else:
        snake.pop()
    if snake[0] in snake[1:]:
        snake=[(cols//2, rows//2)];direction=(0,-1);food=(random.randint(0,cols-1),random.randint(0,rows-1))
        print('Game over! The snake got confused and ate itself. Restarting...')
    screen.fill(BLACK)
    for seg in snake: draw_cell(seg,GREEN)
    draw_cell(food,RED)
    score_surf=font.render(f'Score: {len(snake)-1}',True,WHITE)
    screen.blit(score_surf,(5,5))
    pygame.display.flip()
    clock.tick(10)
