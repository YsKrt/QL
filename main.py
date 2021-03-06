import pygame
from pygame.locals import *
import tkinter as tk
import random
import sys
import os
#import matplotlib.pyplot as plt
SCREEN_SIZE = (640, 480)
xn = 10
yn = 10
class Player():
    def __init__(self,x,y):
        self.x=x
        self.y=y
    def init(self,x,y):
        self.x = x
        self.y = y
class Target():
    def __init__(self,x,y):
        self.x=x
        self.y=y
    def init(self, x, y):
        self.x = x
        self.y = y

class Game():
    def __init__(self):
        self.p=Player(0,0)
        self.t=Target(xn-1,0)
        self.q_table=[0]*xn*yn
        self.obstacle=[0]*xn*yn
        for i in range(yn-1):
            self.obstacle[4+i*yn]=1
        for i in range(6):
            self.obstacle[7+(i+4)*yn]=1
        for i in range(4):
            self.obstacle[6+i+2*yn]=1
    def init(self):
        self.p.init(0,0)
        self.t.init(xn-1,0)
    def control(self,action):
        x=self.p.x
        y=self.p.y
        if action==0 and self.outjudge(x+1,y)==0:
            self.p.x+=1
        if action==1 and self.outjudge(x-1,y)==0:
            self.p.x-=1
        if action==2 and self.outjudge(x,y+1)==0:
            self.p.y+=1
        if action==3 and self.outjudge(x,y-1)==0:
            self.p.y-=1
    def now_state(self):
        return self.p.x+self.p.y*yn
    def get_state(self,x,y):
        if x<0:
            x=0
        if y<0:
            y=0
        if x>xn-1:
            x=xn-1
        if y>yn-1:
            y=yn-1
        return x+y*yn
    def return_reward(self):
        if self.p.x==self.t.x and self.p.y==self.t.y:
            return 1
        return 0
    def draw(self,screen):
        for y in range(yn):
            for x in range(xn):
                q_value=self.q_table[x+y*yn]
                if q_value>255:
                    q_value=255
                if q_value<-255:
                    q_value=-255
                if q_value>0:
                    plus=q_value
                    pygame.draw.rect(screen, (255-plus, 255-plus, 255),
                                     Rect(SCREEN_SIZE[0] / xn * x, SCREEN_SIZE[1] / yn * y,
                                          SCREEN_SIZE[0] / xn,
                                          SCREEN_SIZE[1] / yn))
                if q_value<0:
                    minus=q_value
                    pygame.draw.rect(screen, (255 + minus, 255 + minus, 255 + minus),
                                     Rect(SCREEN_SIZE[0] / xn * x, SCREEN_SIZE[1] / yn * y,
                                          SCREEN_SIZE[0] / xn,
                                          SCREEN_SIZE[1] / yn))
                if self.obstacle[x+y*yn]==1:
                    pygame.draw.rect(screen, (0, 255, 255),
                                     Rect(SCREEN_SIZE[0] / xn * x, SCREEN_SIZE[1] / yn * y,
                                          SCREEN_SIZE[0] / xn,
                                          SCREEN_SIZE[1] / yn))

                if self.p.x==x and self.p.y==y:
                    pygame.draw.rect(screen, (255, 0, 0), Rect(SCREEN_SIZE[0] / xn * x, SCREEN_SIZE[1] / yn * y,
                                                             SCREEN_SIZE[0] / xn,
                                                             SCREEN_SIZE[1] / yn))
                if self.t.x==x and self.t.y==y:
                    pygame.draw.rect(screen, (0, 255, 0), Rect(SCREEN_SIZE[0] / xn * x, SCREEN_SIZE[1] / yn * y,
                                                               SCREEN_SIZE[0] / xn ,
                                                               SCREEN_SIZE[1] / yn ))
                pygame.draw.rect(screen, (0, 0, 0), Rect(SCREEN_SIZE[0]/xn*x, SCREEN_SIZE[1]/yn*y, SCREEN_SIZE[0]/xn,SCREEN_SIZE[1]/yn ), 1)

    def outjudge(self,x,y):
        flag=0
        if x>xn-1 or x<0 or y<0 or y>yn-1:
            flag=1
        elif self.obstacle[x+y*yn]==1:
            flag=2
        return flag
class Learn():
    def __init__(self):
        self.traincount=0
        self.count=1
        self.game=Game()
        self.screen = pygame.display.set_mode(SCREEN_SIZE, pygame.DOUBLEBUF)
        self.q_table=[0]*xn*yn
        pygame.init()
        pygame.display.set_caption(u"Visualize QL")
        self.time=0
        while True:
            if self.traincount>self.count:
                self.update()
            else:

                self.screen.fill((255, 255, 255))
                self.game.draw(self.screen)
                self.update()
                clock = pygame.time.Clock()
                pygame.display.update()
                clock.tick(60)
                for event in pygame.event.get():
                    if event.type == QUIT:
                        pygame.quit()
                        sys.exit()
    def control(self):
        reward=[]
        action=[]
        x=self.game.p.x
        y=self.game.p.y
        if self.game.outjudge(x+1,y)==0:
            reward.append(self.q_table[self.game.get_state(x+1,y)])
            action.append(0)
        if self.game.outjudge(x -1, y)==0:
            reward.append(self.q_table[self.game.get_state(x - 1, y)])
            action.append(1)
        if self.game.outjudge(x,y+1)==0:
            reward.append(self.q_table[self.game.get_state(x,y+1)])
            action.append(2)
        if self.game.outjudge(x,y-1)==0:
            reward.append(self.q_table[self.game.get_state(x,y-1)])
            action.append(3)
        max=-99999999
        maxn=0

        for i in range(len(reward)):
            if reward[i]>max:
                max=reward[i]
                maxn=action[i]
        if max==0 or random.randint(1,100)==1:
            max-=1
            maxn=random.randint(0,3)
        now_state=self.game.now_state()
        if self.q_table[now_state]+10<max:
            self.q_table[now_state]+=10
        elif self.q_table[now_state]-10>max:
            self.q_table[now_state] -= 10
        self.game.control(maxn)
    def update(self):
        self.time += 1
        self.control()
        self.update_qtable()
        self.init()
    def get_reward(self,action):
        if action==1:
            reward=100
        else:
            reward=-1
        return reward
    def update_qtable(self):
        self.q_table[self.game.now_state()]+=self.get_reward(self.game.return_reward())
        self.game.q_table=self.q_table
        pass
    def init(self):
        if self.game.return_reward()==1:
            print(f"{self.count}回目 {self.time}手")
            self.time=0
            self.count+=1
            self.game.init()
if __name__ == '__main__':
    Learn()