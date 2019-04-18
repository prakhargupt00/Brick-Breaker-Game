
# *************************  BRICK BREAKER GAME ******************************

import pygame
import sys
from pygame.locals import * 

# dimensions of objects

screen_size  = (850,480)
brick_width  = 80 
brick_height = 20 
paddle_width = 120
paddle_height = 20
ball_diameter = 24
ball_radius = ball_diameter // 2    # here // is for floor divison gives floor value of divsion 


# Boundaries
max_paddlex =screen_size[0] - paddle_width
max_ballx =  screen_size[0] -ball_diameter
max_bally = screen_size[1] - ball_diameter

#Y coordinates
paddley = screen_size[1]-paddle_height -10 

#colors
white = (255,255,255)
purple =(91,44,111)
turqoise =(3,155,229)
grey2 =(44,62,80)
red =(255,0,0)
yellow =(255,255,0)

#States
state_ballinpaddle =0 
state_inplay =1
state_won =2
state_gameover =3

class brickbreaker():

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(screen_size)
        pygame.display.set_caption("BrickBreaker")
        self.clock = pygame.time.Clock()


        self.font = pygame.font.SysFont('Lucida Sans Roman' ,20)
        self.init_game()

    def init_game(self):
        self.lives =3 
        self.score =0 
        self.state = state_ballinpaddle

        self.paddle =pygame.Rect(365,paddley,paddle_width,paddle_height)
        self.ball =pygame.Rect(365,paddley-ball_diameter,ball_diameter ,ball_diameter)           #ball approximated to the rect object

        self.ballvel =[5,-5]           #for the ball velocity 

        self.create_bricks()



    def create_bricks(self):
        y_brick = 30
        self.bricks =[]

        for i in range(7):
            x_brick = 30
            for j in range(9):
                self.bricks.append(pygame.Rect(x_brick ,y_brick,brick_width,brick_height))
                x_brick += brick_width+8
            y_brick += brick_height +6


    def draw_bricks(self):
        for brick in self.bricks:
            pygame.draw.rect(self.screen,red,brick)

    def check_input(self):
        keys =pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            self.paddle.left -=10 
            if self.paddle.left < 0:
                self.paddle.left =0 

        if keys[pygame.K_RIGHT]:
            self.paddle.left +=10
            if self.paddle.left > max_paddlex:
                self.paddle.left =max_paddlex

        if keys[pygame.K_SPACE] and self.state == state_ballinpaddle :
            self.ballvel =[5,-5]
            self.state = state_inplay

        if keys[pygame.K_q] and (self.state == state_gameover or self.state == state_won) :
            pygame.display.quit()
            pygame.quit()
            sys.exit()

        if keys[pygame.K_RETURN ] and (self.state == state_gameover or self.state == state_won) :   #enter = return 
            self.init_game() 

    def move_ball(self) :
        self.ball.left += self.ballvel[0]
        self.ball.top += self.ballvel[1]

        if self.ball.left <= 0 :
            self.ball.left = 0
            self.ballvel[0] = -self.ballvel[0]

        elif self.ball.left >= max_ballx :
            self.ball.left = max_ballx
            self.ballvel[0] = -self.ballvel[0]

        if self.ball.top < 0 :
            self.ballvel[1] =-self.ballvel[1]
            self.ball.top = 0

        # elif self.ball.top >= max_bally:
        #     self.ball.top =max_bally

    def handle_coll(self):
        for brick in self.bricks :
            if self.ball.colliderect(brick) :
                self.score +=1
                self.ballvel[1] = -self.ballvel[1]
                self.bricks.remove(brick)
                break

        if len(self.bricks) == 0 :
            self.state = state_won

        if self.ball.colliderect(self.paddle) :
            self.ball.top =paddley - ball_diameter
            self.ballvel[1] = -self.ballvel[1]

        elif self.ball.top > self.paddle.top:
            self.lives -= 1
            if self.lives > 0:
                self.state = state_ballinpaddle
            else:
                self.state =state_gameover

        
    def show_stats(self) :
        font_surface = self.font.render("SCORE : " + str(self.score) + "  LIVES : " + str(self.lives) , False ,white)
        self.screen.blit(font_surface,(600,5))

    def show_message(self,message):
        size = self.font.size(message)
        font_surface =self.font.render(message,False,white)
        x = (screen_size[0]- size[0]) / 2
        y = (screen_size[1] - size[1]) / 2
        self.screen.blit(font_surface , (x,y) )

    def run(self):

        while True:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.display.quit()
                    pygame.quit()
                    sys.exit()

            self.clock.tick(65)
            self.screen.fill(turqoise)
            self.check_input()  

            
            if self.state == state_ballinpaddle:
                self.ball.left = self.paddle.left + paddle_width / 2 
                self.ball.top =  self.paddle.top - ball_diameter
                self.show_message("Press Space to launch the ball")

            elif self.state == state_gameover:
                self.show_message("Game Over , Press Enter to Play again or Q to quit ")

            elif self.state == state_won:
                self.show_message("You Won! Press enter to play again or q to quit ")

            elif self.state == state_inplay:
                self.move_ball()
                self.handle_coll() 


            #Draw the paddle  
            pygame.draw.rect(self.screen ,purple ,self.paddle)

            #Draw the ball
            pygame.draw.circle(self.screen, yellow ,(self.ball.left+ ball_radius ,self.ball.top + ball_radius) ,ball_radius)

            self.draw_bricks()

            self.show_stats()
            pygame.display.update()

            


game =brickbreaker()
game.run() 

