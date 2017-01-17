# coding=utf-8
# import modules used here -- sys is a very standard one
import sys
import time
import random
import math


'''建立電梯'''
class elevator:
    ''' floor=電梯在第幾樓
        dir=up,down,stop
        psg=number of people 0~10
        addTime=開關啓閉進出時間, default=0
        goToFloor=控制要去的樓層, default=0
    '''
    def __init__(self, floor , dir , psg, addTime=0,goToFloor=0):
        
        self.floor = floor #電梯在第幾樓
        self.dir=dir #up,down,stop 
        self.psg=psg #number of people 0~10
        self.addTime=addTime #開關啓閉進出時間
        self.goToFloor=goToFloor #控制要去的樓層
    '''進電梯'''
    def getIn(self,psg):
        if len(self.psg)<10:
            self.psg.append(psg)
    '''出電梯'''
    def getOut(self,psg):
        self.psg.remove(psg)
    '''超重逼逼'''
    def notFull(self,psg):
        if len(self.psg)<10:
            return True
        else:
            return False

    '''電梯開關門'''
    def takeElevator(self,position):
        tempDir=False
        for psg in list(self.psg):
            if self.floor==psg[1]: # elevator.floor樓有人要離開電梯                                        
                tempDir=True #電梯停不停
                self.getOut(psg)#離開電梯
                self.addTime+=1#每離開一個人花費一秒
        if position[self.floor] and not self.goToFloor: #elevator.floor樓有人要搭電梯
            tempDir=True #電梯停不停 
            for psg in list(position[self.floor]): #elevator.floor樓所有乘客
                if self.notFull:#電梯未滿載
                    self.getIn(psg)#進入電梯
                    position[self.floor].remove(psg)#離開樓層
                    self.addTime+=1#每進入一個人花費一秒
        elif self.floor==self.goToFloor:#抵達要求樓層
            tempDir=True #電梯停不停
            for psg in list(position[self.floor]): #elevator.floor樓所有乘客
                if self.notFull:#電梯未滿載
                    self.getIn(psg)#進入電梯
                    position[self.floor].remove(psg)#離開樓層
                    self.addTime+=1#每進入一個人花費一秒
            self.goToFloor=0

        return tempDir
    '''選樓層'''
    def moveToNextFloor(self,position):
    
    
        f=self.floor
        '''1~max~1'''
        if self.dir=='up'and f < self.findMaxFloor(position): #電梯方向 18:#
            f+=1
        else:
            self.dir='down'
        if self.dir=='down' and f > self.findMinFloor(position): #電梯方向 0:#
            f-=1
        else:
            self.dir='up'
        self.floor= f
    '''找最 高 要到幾樓'''
    def findMaxFloor(self,b):
        a=self.psg
        tempA = 0
        tempB = 0
        for x in b:
            if x:
                tempB=x[0][0]#等待電梯的人最高樓層       
        if a:
            tempA=max(a,key=lambda item:item[1])[1]#抓乘客抵達樓層最大值
         
        return max(tempA,tempB)

    '''找最 低 要到幾樓'''
    def findMinFloor(self,b):
        a=self.psg
        tempA = 0
        tempB = 0
        for x in b:
            if x:
                tempB=x[0][0]#等待電梯的人最低樓層
                break   
        if a:
            tempA=min(a,key=lambda item:item[1])[1]#抓乘客抵達樓層最小值
         
        return min(tempA,tempB)

'''是否還有人在等電梯'''
def isAnyoneWait(pasition):
    for p in pasition:
        if p:
            return True
    return False

def chooseFloor(position):
    lengths=[]
    for p in position:
        lengths.append(len(p))
    
    return lengths

def maybeFaster(E,position):
    nums=chooseFloor(position)
    E.goToFloor=nums.index(max(nums))
    if E.goToFloor > E.floor:
        E.dir='up'
    else:
        E.dir='down'

def maybeFaster2(E,position):
    nums=chooseFloor(position)
    nums.pop(nums.index(max(nums))) 
    E.goToFloor=nums.index(max(nums))
    if E.goToFloor > E.floor:
        E.dir='up'
    else:
        E.dir='down'


def main():
    #計時
    totalTime=0
    muti=1
    for i in range(muti):        
        '''建立乘客'''
        #a=[(random.randint(1, 18),random.randint(1, 18)) for _ in range(180)]#產生10個1~1000的亂數
        #a=[(1, 5), (1, 3), (1, 14), (1, 11), (1, 6), (1, 13), (1, 15), (1, 7), (1, 9), (1, 9), (1, 9), (18, 9), (2, 9)]
        a=[(17, 5), (11, 3), (13, 8), (5, 16), (18, 16), (3, 6), (7, 1), (2, 1), (6, 13), (18, 8), (15, 9), (1, 8), (9, 12), (7, 3), (13, 6), (9, 10), (4, 6), (17, 16), (17, 14), (13, 16), (18, 10), (12, 18), (18, 8), (2, 4), (3, 1), (17, 13), (9, 11), (6, 9), (17, 3), (7, 14), (15, 10), (7, 1), (2, 16), (3, 16), (4, 2), (3, 4), (4, 7), (8, 2), (14, 18), (1, 10), (10, 5), (3, 15), (15, 9), (9, 2), (16, 7), (18, 11), (1, 16)]	
        
        #去除重複
        for t in a:
            if t[0]== t[1] :
                a.remove(t)
        
        #依照抵達樓層排序
        #a.sort(key=lambda tup: tup[1])
        #print ("*序列",a)
        
        #依照所在樓成排序
        a.sort()
                
        position=[[] for i in range(19)]#list[0:18]的二維list
        #每層樓要搭電梯的人 放在同一層樓
        for t in a:
            position[t[0]].append(t)
        #print (position)
        
        #建立電梯
        E_1 =elevator(9,'up',[])
        E_2 =elevator(9,'up',[])
        E_3 =elevator(9,'up',[])

        #顯示每層樓要搭電梯的人
        for p in position:
            if p:
                print (p)
        

        ##1~18樓
        while isAnyoneWait(position) or E_1.psg or E_2.psg or E_3.psg :
            #假設電梯移動一層樓的時間
            totalTime+=1

            '''E1'''
            if not E_1.psg:
                #print('E1 Idle')
                maybeFaster(E_1,position)

            if E_1.addTime==0:            
                E_1.moveToNextFloor(position)#移動電梯            
                if E_1.takeElevator(position):#True停 False不停
                    E_1.addTime+=4#電梯開關加啟動煞車時間                
                    print('\nFloor=',E_1.floor,' 等電梯的人=',position,'\n\televator=1 乘客=',len(E_1.psg),E_1.psg)
            else:
                E_1.addTime-=1

            '''E2'''
            if not E_2.psg:
                #print('E2 Idle')
                maybeFaster2(E_2,position)

            if E_2.addTime==0:    
                E_2.moveToNextFloor(position)#移動電梯
                if E_2.takeElevator(position):#True停 False不停
                    E_2.addTime+=4 #電梯開關加啟動煞車時間
                    print('\nFloor=',E_2.floor,' 等電梯的人=',position,'\n\televator=2 乘客=',len(E_2.psg),E_2.psg)
            else:
                E_2.addTime-=1

            '''E3'''
            #if not E_3.psg:
                #print('E3 Idle')
                

            if E_3.addTime==0:    
                E_3.moveToNextFloor(position)#移動電梯
                if E_3.takeElevator(position):#True停 False不停
                    E_3.addTime+=4 #電梯開關加啟動煞車時間
                    print('\nFloor=',E_3.floor,' 等電梯的人=',position,'\n\televator=3 乘客=',len(E_3.psg),E_3.psg)
            else:
                E_3.addTime-=1  
            
            #print(E_1.addTime,'\t',E_2.addTime,'\t',E_3.addTime)
            #end while
        #print(totalTime)
    print(totalTime/muti)

if __name__ == '__main__':
    main()
    input('...')