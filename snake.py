import cv2
import numpy as np
import time
import pygame
import random

blockSize=30
frameSize=690

pygame.init()

class point():
    def __init__(self,x,y):
        self.x=x
        self.y=y

    def __add__(self,other):
        return point((self.x + other.x * blockSize) , (self.y + other.y * blockSize))
    
    def __eq__(self,other):
        return (self.x == other.x and self.y == other.y)


class food():
    def __init__(self):
        self.pos = point(random.randint(0,23),random.randint(0,23))

    def generateFood(self,canvas):
        self.pos.x = random.randint(0,22)*blockSize
        self.pos.y = random.randint(0,22)*blockSize
        canvas = cv2.rectangle(canvas, (self.pos.x , self.pos.y) , (self.pos.x + blockSize ,self.pos.y + blockSize), (255,0,0), -1)
        return canvas

    def posFood(self,canvas):
        #draw the food again
        canvas = cv2.rectangle(canvas, (self.pos.x , self.pos.y) , (self.pos.x + blockSize ,self.pos.y + blockSize), (255,0,0), -1)

    def eatFood(self,snake,canvas):
        #checking if snake has eaten the food
        if snake.bodyArray[0] == self.pos:
            canvas = cv2.rectangle(canvas, (self.pos.x , self.pos.y) , (self.pos.x + blockSize ,self.pos.y + blockSize), (20,20,20), -1)
            self.generateFood(canvas)
            return True
        return False

class snake():
    def __init__(self):
        self.bodyArray=[point(0,0)]
        self.dirs={
            'left' : point(-1,0),
            'right' : point(1,0),
            'up' : point(0,-1),
            'down' : point(0,1)
        }
        self.curDir='right'
        self.F = food()
        self.Die = False

    
    def update(self):
        for i in range(len(self.bodyArray)):
            self.bodyArray[i] = self.bodyArray[i] + self.dirs[self.curDir]
            print(self.bodyArray[i].x,self.bodyArray[i].y)
        self.die()
        #time.sleep(0.25)


    def die(self):
        if self.bodyArray[0].x < 0 or self.bodyArray[0].x > 630 or self.bodyArray[0].y < 0 or self.bodyArray[0].y > 630:
            print('dead')
            self.Die = True


    def display(self):
        frame = 1
        while not(self.Die):
            canvas=20*np.ones((frameSize,frameSize),np.uint8)
            canvas = cv2.cvtColor(canvas,cv2.COLOR_GRAY2BGR)
            
            if frame == 1:
                #when the game starts
                self.F.generateFood(canvas)
                frame+=1
            
            #drawing food on canvas
            self.F.posFood(canvas)


            #drawing snake on canvas
            for blk in self.bodyArray:
                cv2.rectangle(canvas, (blk.x , blk.y) , (blk.x + blockSize ,blk.y + blockSize), (255,255,255), -1)
            cv2.imshow("game",canvas)

            fd = self.F.eatFood(self,canvas)
            prevPos = self.bodyArray[-1]
            self.update()
            if fd:
                self.bodyArray.append(prevPos)
            


            #capturing key presses
            keyPress = cv2.waitKeyEx(250)
            if keyPress == 27:
                break
            
            elif keyPress == 65364 and (self.curDir != 'up' or self.curDir != 'down'):
                self.curDir = 'down'
            elif keyPress == 65361 and (self.curDir != 'right' or self.curDir != 'left'):
                self.curDir = 'left'
            elif keyPress == 65363 and (self.curDir != 'left' or self.curDir != 'right'):
                self.curDir = 'right'
            elif keyPress == 65362 and (self.curDir != 'down' or self.curDir != 'up'):
                self.curDir = 'up'
            print(keyPress)
            


def main():
    S = snake()
    S.display()

#    if cv2.waitKey(0)==27:
#        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
