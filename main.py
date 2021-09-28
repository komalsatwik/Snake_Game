import pygame
from pygame.locals import *
import time
import random

SIZE = 40

class Apple:
    def __init__(self,parent_screen):
        self.apple = pygame.image.load("resources/apple.jpg").convert()
        self.parent_screen = parent_screen
        self.x = SIZE*3
        self.y = SIZE*3

    def draw(self):
        self.parent_screen.blit(self.apple,(self.x,self.y))
        pygame.display.flip()

    def place(self):
        self.x = random.randint(0,24)*SIZE
        self.y = random.randint(0,14)*SIZE


class player:
    def __init__(self,parent_screen,length):
        self.parent_screen = parent_screen
        self.length = length
        self.block = pygame.image.load("resources/block.jpg").convert()
        self.x = [SIZE]*length
        self.y = [SIZE]*length
        self.direction = 'right'

    def increase(self):
        self.length += 1
        self.x.append(-1)
        self.y.append(-1)


    def draw(self):
        
        for i in range(self.length):
            self.parent_screen.blit(self.block,(self.x[i],self.y[i]))
        pygame.display.flip()

    def move_left(self):
        self.direction = 'left'

    def move_right(self):
        self.direction = 'right'

    def move_up(self):
        self.direction = 'up'

    def move_down(self):
        self.direction = 'down'

    def walk(self):
        for i in range(self.length-1,0,-1):
            self.x[i] = self.x[i-1]
            self.y[i] = self.y[i-1]

        if self.direction == 'left':
            self.x[0] -= SIZE

        if self.direction == 'right':
            self.x[0] += SIZE
        
        if self.direction == 'up':
            self.y[0] -= SIZE
        
        if self.direction == 'down':
            self.y[0] += SIZE
        
        self.draw()

class Game:
    def __init__(self):
        pygame.init()

        self.surface = pygame.display.set_mode((1000,600))
        pygame.mixer.init()
        self.play_bgm()

        self.background()
        self.player = player(self.surface,2)
        self.player.draw()
        self.apple = Apple(self.surface)
        self.apple.draw()
    
    def play_sound(self,sound):
        sound = pygame.mixer.Sound(f"resources/{sound}.mp3")
        pygame.mixer.Sound.play(sound)
    def points(self):
        font = pygame.font.SysFont('arial',30)
        score = font.render(f"Score:{self.player.length}",True,(0,0,0))
        self.surface.blit(score,(800,10))
        
    def play_bgm(self):
        pygame.mixer.music.load("resources/bg_music_1.mp3")
        pygame.mixer.music.play()
    
    def background(self):
        background = pygame.image.load("resources/background.jpg")
        self.surface.blit(background,(0,0))

    def play(self):
        self.background()
        self.player.walk()
        self.apple.draw()
        self.points()
        pygame.display.flip()

        if self.collision(self.player.x[0],self.player.y[0],self.apple.x,self.apple.y):
            self.play_sound("1_snake_game_resources_ding")
            
            self.player.increase()
            self.apple.place()

        for i in range(3,self.player.length):
            if self.collision(self.player.x[0],self.player.y[0],self.player.x[i],self.player.y[i]):
                self.play_sound("1_snake_game_resources_crash")
               
                raise "Game Over"

        if not self.collision_border(self.player.x[0],self.player.y[0]):
            self.play_sound("1_snake_game_resources_crash")
            raise "Game Over"

            
    def collision_border(self,x,y):
        if x>=0 and x<=1000:
            if y>=0 and y<=600:
                return True
        return False
    def collision(self,x1,y1,x2,y2):
        if x1 >= x2 and x1 < x2 + SIZE:
            if y1 >= y2 and y1 < y2 + SIZE:
                return True
        return False

    def game_over(self):
        self.background()
        font = pygame.font.SysFont('arial',30)
        line1 = font.render(f"Score:{self.player.length}",True,(0,0,0))
        self.surface.blit(line1,(200,300))
        line2 = font.render("To play hit Enter.To exit click escape",True,(0,0,0))
        self.surface.blit(line2,(200,350))
        pygame.display.flip()
        pygame.mixer.music.pause()

    def reset(self):
        self.player = player(self.surface,2)
        self.apple = Apple(self.surface)

    def run(self):
        running = True
        pause = False
        while running:
            for event in pygame.event.get():

                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False
                    
                    if event.key == K_RETURN:
                        pygame.mixer.music.unpause()
                        pause = False

                    if not pause:

                        if event.key == K_UP:
                            self.player.move_up()
                        if event.key == K_DOWN:
                            self.player.move_down()
                        if event.key == K_RIGHT:
                            self.player.move_right()
                        if event.key == K_LEFT:
                            self.player.move_left()

                elif event.type == QUIT:
                    running = False
                 
            try:
                if not pause:
                    self.play()
            except Exception as e:
                self.game_over()
                pause = True
                self.reset()
            
            if self.player.length < 5:
                time.sleep(0.25)
            elif self.player.length <15:
                time.sleep(0.2)
            time.sleep(0.1)



if __name__ == "__main__":
    
   game = Game()
   game.run()

    

  