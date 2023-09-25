#import pygame
import pygame, sys, random

def draw_floor():
    screen.blit(floor_surf,(floor_x,616))
    screen.blit(floor_surf,(floor_x+394,616))

def create_pipe():
    random_pipe_y = random.choice(pipe_height)
    bottom_pipe = pipe_surf.get_rect(midtop = (479,random_pipe_y))
    top_pipe = pipe_surf.get_rect(midbottom =(479, random_pipe_y-205))
    return bottom_pipe,top_pipe
  
def move_pipes(pipes):
    for pipe in pipes:
        pipe.centerx  -= 4
    return pipes

def draw_pipes(pipes):
    for pipe in pipes:
        if pipe.bottom >= 700:
            screen.blit(pipe_surf,pipe)
        else:
            flip_pipe = pygame.transform.flip(pipe_surf,False,True)
            screen.blit(flip_pipe,pipe)

def check_collision(pipes):
    global can_score
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            can_score = True
            return False
    if bird_rect.top <= -68 or bird_rect.bottom >= 616:
        return False
    return True

def rotate_bird(bird):
    new_bird = pygame.transform.rotozoom(bird,-bird_movement *1.25,1)
    return new_bird

def bird_animation():
    new_bird = bird_frames[bird_index]
    new_bird_rect = new_bird.get_rect(center =(68,bird_rect.centery))
    return new_bird,new_bird_rect

def score_display(game_state):
    if game_state == "main_game":
        score_surf = game_font.render(str(int(score)),True,(255,255,255))
        score_rect = score_surf.get_rect(center =(197,68))
        screen.blit(score_surf,score_rect)
    if game_state == "game_over":
        score_surf = game_font.render(f"score : {int(score)}",True,(255,255,255))
        score_rect = score_surf.get_rect(center =(197,68))
        screen.blit(score_surf,score_rect)

def pipe_score_check():
    global score,can_score
    if pipe_list :
        for pipe in pipe_list:
            if 65 < pipe.centerx < 72 and can_score:
                score += 1
                can_score = False
            if pipe.centerx < 0 :
                can_score = True

pygame.init()
screen = pygame.display.set_mode((393,700))
clock = pygame.time.Clock()
game_font = pygame.font.Font("04B_19.TTF",30)
#game variables
game_active = True
can_score = True
score = 0
gravity = 0.25
bird_movement = 0

bg_surf = pygame.image.load("assets/background-day.png").convert()
bg_surf =pygame.transform.rotozoom(bg_surf,0,1.368).convert()

floor_surf = pygame.image.load("assets/base.png").convert()
floor_surf = pygame.transform.rotozoom(floor_surf,0,1.368)
floor_x = 0

bird_downflap = pygame.transform.rotozoom(pygame.image.load("assets/bluebird-downflap.png"),0,1.368)
bird_midflap = pygame.transform.rotozoom(pygame.image.load("assets/bluebird-midflap.png"),0,1.368)
bird_upflap = pygame.transform.rotozoom(pygame.image.load("assets/bluebird-upflap.png"),0,1.368)
bird_frames = [bird_downflap,bird_midflap,bird_upflap]
bird_index = 0
bird_surf = bird_frames[bird_index]
bird_rect = bird_surf.get_rect(center = (68,350))

BIRDFLAP = pygame.USEREVENT + 1
pygame.time.set_timer(BIRDFLAP,200)

pipe_surf = pygame.image.load("assets/pipe-green.png").convert()
pipe_surf = pygame.transform.rotozoom(pipe_surf,0,1.368)
pipe_list = []
pipe_height =[274,410,547]
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE,1200)


game_over_surf = pygame.image.load("assets/message.png").convert_alpha()
game_over_surf = pygame.transform.rotozoom(game_over_surf,0,1.368)
game_over_rect = game_over_surf.get_rect(center = (197,350))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bird_movement = 0
                bird_movement -= 10
            if event.key == pygame.K_SPACE and game_active == False:
                game_active = True
                pipe_list.clear()
                bird_rect.center = (68,350)
                bird_movement = 0
                score = 0

        if event.type == SPAWNPIPE:
            pipe_list.extend(create_pipe())
        
        if event.type == BIRDFLAP:
            if bird_index < 2:
               bird_index += 1
            else:
                bird_index = 0
        bird_surf,bird_rect = bird_animation()        
    screen.blit(bg_surf,(0,0))

   
    if game_active:   
        #bird
        bird_movement += gravity
        rotated_bird = rotate_bird(bird_surf)
        bird_rect.centery += bird_movement
        screen.blit(rotated_bird,bird_rect)
        game_active= check_collision(pipe_list)

        #pipes
        pipe_list =  move_pipes(pipe_list)
        draw_pipes(pipe_list)

        #score 
        score_display("main_game")
        pipe_score_check()

    else:
        screen.blit(game_over_surf,game_over_rect)
        score_display("game_over")
     #floor
    floor_x -= 1
    draw_floor()
    if floor_x <= -394:
        floor_x = 0
    pygame.display.update()
    clock.tick(120)
