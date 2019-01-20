import cv2
import numpy as np
import time
#from msvcrt import getch

blockSize=30

class point():
    def __init__(self,x,y):
        self.x=x
        self.y=y

    def __add__(self,other):
        return point((self.x + other.x * blockSize) , (self.y + other.y * blockSize))
    
    def __eq__(self,other):
        return (self.x == other.x and self.y == other.y)


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
    
    def update(self):
        for i in range(len(self.bodyArray)):
            self.bodyArray[i] = self.bodyArray[i] + self.dirs[self.curDir]
            print(self.bodyArray[i].x,self.bodyArray[i].y)
            
        time.sleep(0.25)
        
    def getDir(self,keyPress):
        print(keyPress)
        """
        if(keyPress == 72):
            self.curDir = 'up'
            print('direction changed to up')
        elif(keyPress == 80):
            self.curDir = 'down'
            print('direction changed to down')
        elif(keyPress == 75):
            self.curDir = 'left'
            print('direction changed to left')
        elif(keyPress == 77):
            self.curDir = 'right'
            print('direction changed to right')
        else:
            pass
        """

    def display(self):
        while True:
            canvas=20*np.ones((690,690),np.uint8)
            cv2.cvtColor(canvas,cv2.COLOR_GRAY2BGR)
            for blk in self.bodyArray:
                cv2.rectangle(canvas, (blk.x , blk.y) , (blk.x + blockSize ,blk.y + blockSize), (255,0,0), -1)
            cv2.imshow("game",canvas)
            self.update()
            keyPress = cv2.waitKeyEx(1)
            if keyPress == 27:
                break
            elif keyPress == 65364:
                self.curDir = 'down'
            elif keyPress == 65361:
                self.curDir = 'left'
            elif keyPress == 65363 :
                self.curDir = 'right'
            elif keyPress == 65362 :
                self.curDir = 'up'
            print(keyPress)
            


def main():
    S = snake()
    S.display()

#    if cv2.waitKey(0)==27:
#        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
