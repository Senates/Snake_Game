import pygame, os , random , sys
from pygame.math import Vector2
pygame.init()


class SNAKE:
    def __init__(self):
        self.body = [Vector2(10,10),Vector2(9,10),Vector2(8,10)]
        self.direction = Vector2(1,0)
        self.new_block = False

    def draw_snake(self):
        for block in self.body:
            block_rect = pygame.Rect(block.x * cell_size,block.y * cell_size,cell_size,cell_size)
            pygame.draw.rect(screen,(255, 0, 185),block_rect)


    def move_snake(self):
        if self.new_block == True:
            body_copy = self.body[:] #takes the values of self.body -1 (last one)
            body_copy.insert(0,body_copy[0] + self.direction)
            self.body = body_copy[:]
            self.new_block = False
        else:
            body_copy = self.body[:-1] #takes the values of self.body -1 (last one)
            body_copy.insert(0,body_copy[0] + self.direction)
            self.body = body_copy[:]

    def add_block(self):
        self.new_block = True

    def reset(self):
        self.body = [Vector2(10,10),Vector2(9,10),Vector2(8,10)]

class FRUIT:
    def __init__(self):
        self.x = random.randint(0,cell_num - 1)
        self.y = random.randint(0,cell_num - 1)
        self.pos = Vector2(self.x,self.y)

    def draw_fruit(self):
        fruit_rect = pygame.Rect(self.x * cell_size,self.y *cell_size,cell_size,cell_size) #xpos,ypos,width,height
        pygame.draw.rect(screen,pygame.Color('White'),fruit_rect) #location,color,rectangle wanted to draw

    def randomize(self):
        self.x = random.randint(0,cell_num - 1)
        self.y = random.randint(0,cell_num - 1)
        self.pos = Vector2(self.x,self.y)

class MAIN:
    def __init__(self):
        self.snake = SNAKE()
        self.fruit = FRUIT()

    def update(self):
        self.snake.move_snake()
        self.check_collision()
        self.check_fail()

    def draw_elements(self):
        self.fruit.draw_fruit()
        self.snake.draw_snake()
        self.draw_score()

    def check_collision(self):
        if self.fruit.pos == self.snake.body[0]:
            self.fruit.randomize()
            self.snake.add_block()
            
        for block in self.snake.body[1:]:
            if block == self.fruit.pos:
                self.fruit.randomize()



    def check_fail(self):
        if not 0 <= self.snake.body[0].x < cell_num or not 0 <= self.snake.body[0].y < cell_num:
            self.game_over()
        
        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
                self.game_over()

    def game_over(self):
        self.restart()

    def restart(self):
        self.snake.reset()
        global score_text
        endfont = pygame.font.Font(None,48)
        endtext = endfont.render("YOU   DIED!",True,(255,0,0))
        endtext2 = endfont.render("PRESS   'SPACE'   TO  RESTART!",True,(255,0,0))
        endscore = endfont.render("FINAL SCORE:  " + score_text,True,(255,0,0))
        screen.blit(endtext,(320,100))
        screen.blit(endtext2,(160,280))
        screen.blit(endscore,(280,400))
        var = True
        while var:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        main_running = False
                        start_running = True
                        var = False

            pygame.display.update()

    def draw_score(self):
        global score_text
        score_text = str(len(self.snake.body) - 3)
        score_surface = game_font.render(score_text,True,(255,0,0)) #Text, anti aliasing(smoothness),color
        score_x=int(15)
        score_y=int(15)
        score_rect = score_surface.get_rect(center = (score_x,score_y))
        screen.blit(score_surface,score_rect)
    

#Variables
cell_size = 40
cell_num = 20
screen = pygame.display.set_mode((cell_num * cell_size,cell_num * cell_size))
clock = pygame.time.Clock()  #defining clock to esentially set/limit FPS
game_font = pygame.font.Font(None,30)
pygame.display.set_caption('Snake Game')

game_speed = 150

SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE,game_speed)
main_game = MAIN()
main_running = False
start_running = True

def start_screen():
    screen.fill((0,0,0)) 
    image = pygame.image.load(r'D:\Programming\Tech_Python\snakegameimage.png')
    screen.blit(image,(100,100))

while start_running: #start loop
    start_screen()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                main_running = True
                start_running = False
                end_running = False
    pygame.display.update()
    
while main_running: #Main event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == SCREEN_UPDATE:
            main_game.update()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                if main_game.snake.direction.y != 1:
                    main_game.snake.direction = Vector2(0,-1)
            if event.key == pygame.K_DOWN:
                if main_game.snake.direction.y != -1:
                    main_game.snake.direction = Vector2(0,1)
            if event.key == pygame.K_LEFT:
                if main_game.snake.direction.x != 1:
                    main_game.snake.direction = Vector2(-1,0)
            if event.key == pygame.K_RIGHT:
                if main_game.snake.direction.x != -1:
                    main_game.snake.direction = Vector2(1,0)


    screen.fill(pygame.Color('Black'))
    main_game.draw_elements()
    clock.tick(144) #setting the fps
    pygame.display.update()
