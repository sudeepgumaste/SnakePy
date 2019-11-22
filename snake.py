import cv2
import numpy as np
import time
import random
import sys

blockSize=30
frameSize=690


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
        self.pos.x = random.randint(1,21)*blockSize
        self.pos.y = random.randint(1,21)*blockSize
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
        if sys.platform=='linux':
            self.left = 65361
            self.right = 65363
            self.top = 65362
            self.down = 65364
        else :
            self.left = 2424832
            self.right = 2555904
            self.top = 2490368
            self.down = 2621440

    
    def update(self,eat):
        last = self.bodyArray[-1]
                
        size=len(self.bodyArray)-1
        while(size>0):
            self.bodyArray[size]=self.bodyArray[size-1]
            size-=1
        
        
        self.bodyArray[0] = self.bodyArray[0] + self.dirs[self.curDir]
 

        if eat:
            #if food is eaten increase the length
            self.bodyArray.append(last)


    def death(self):
        if self.bodyArray[0].x < 0 or self.bodyArray[0].x > 630 or self.bodyArray[0].y < 0 or self.bodyArray[0].y > 630:
            self.Die = True
        for i in range(1,len(self.bodyArray)):
            if self.bodyArray[i] == self.bodyArray[0]:
                self.Die=True
        
        if self.Die:
            print('dead')


    def display(self):
        frame = 1
        while not(self.Die):
            score = len(self.bodyArray) - 1
            canvas=20*np.ones((frameSize,frameSize),np.uint8)
            canvas = cv2.cvtColor(canvas,cv2.COLOR_GRAY2BGR)
            
            cv2.putText(canvas,"Score : " + str(score),(5,20), cv2.FONT_HERSHEY_SIMPLEX,0.55,(0,255,0))

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
            self.death()

            eat = self.F.eatFood(self,canvas)
            self.update(eat)
            


            #capturing key presses
            tKey = time.time()
            keyPress = cv2.waitKeyEx(250)
            tKeyDown = time.time() - tKey
            waitTime = 250/1000 -tKeyDown
            if keyPress == 27:
                break
            
            elif keyPress == self.down and (self.curDir != 'up' or self.curDir != 'down'):
                self.curDir = 'down'
                time.sleep(waitTime)

            elif keyPress == self.left and (self.curDir != 'right' or self.curDir != 'left'):
                self.curDir = 'left'
                time.sleep(waitTime)

            elif keyPress == self.right and (self.curDir != 'left' or self.curDir != 'right'):
                self.curDir = 'right'
                time.sleep(waitTime)
            
            elif keyPress == self.top and (self.curDir != 'down' or self.curDir != 'up'):
                self.curDir = 'up'
                time.sleep(waitTime)
            
        for i in range(240):
            score = len(self.bodyArray) - 1
            canvas=20*np.ones((frameSize,frameSize),np.uint8)
            canvas = cv2.cvtColor(canvas,cv2.COLOR_GRAY2BGR)

            cv2.putText(canvas,"Score : " + str(score),(5,20), cv2.FONT_HERSHEY_SIMPLEX,0.55,(0,255,0))
            
            cv2.putText(canvas,"Game Over",(70,frameSize//2), cv2.FONT_HERSHEY_COMPLEX,3,(0,255,0))

            if i%2 == 1:
                for blk in self.bodyArray:
                    cv2.rectangle(canvas, (blk.x , blk.y) , (blk.x + blockSize ,blk.y + blockSize), (255,255,255), -1)
            
            cv2.imshow("game",canvas)
            time.sleep(0.5)
            

            if cv2.waitKey(1) == 27:
                cv2.destroyAllWindows()
                break

            


def main():
    S = snake()
    S.display()

if __name__ == "__main__":
    main()
