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
        self.pos.x = random.randint(0,22)*30
        self.pos.y = random.randint(0,22)*30
        canvas = cv2.rectangle(canvas, (self.pos.x , self.pos.y) , (self.pos.x + blockSize ,self.pos.y + blockSize), (255,0,0), -1)
        return canvas

    def posFood(self,canvas):
        canvas = cv2.rectangle(canvas, (self.pos.x , self.pos.y) , (self.pos.x + blockSize ,self.pos.y + blockSize), (255,0,0), -1)

    def eatFood(self,snake,canvas):
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

    
    def update(self):
        for i in range(len(self.bodyArray)):
            self.bodyArray[i] = self.bodyArray[i] + self.dirs[self.curDir]
            print(self.bodyArray[i].x,self.bodyArray[i].y)
            
        time.sleep(0.20)
        
    def getDir(self,keyPress):
        print(keyPress)

    def display(self):
        frame = 1
        while True:
            canvas=20*np.ones((frameSize,frameSize),np.uint8)
            canvas = cv2.cvtColor(canvas,cv2.COLOR_GRAY2BGR)
            
            if frame == 1:
                self.F.generateFood(canvas)
                frame+=1
            
            self.F.posFood(canvas)

            for blk in self.bodyArray:
                cv2.rectangle(canvas, (blk.x , blk.y) , (blk.x + blockSize ,blk.y + blockSize), (255,255,255), -1)
            cv2.imshow("game",canvas)
            self.update()
            


            #capturing key presses
            keyPress = cv2.waitKeyEx(4)
            if keyPress == 27:
                break
            
            elif keyPress == 65364 and self.curDir != 'up':
                self.curDir = 'down'
            elif keyPress == 65361 and self.curDir != 'right':
                self.curDir = 'left'
            elif keyPress == 65363 and self.curDir != 'left':
                self.curDir = 'right'
            elif keyPress == 65362 and self.curDir != 'down':
                self.curDir = 'up'
            print(keyPress)
            


def main():
    S = snake()
    S.display()

#    if cv2.waitKey(0)==27:
#        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
