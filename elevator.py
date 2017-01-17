# coding=utf-8
# import modules used here -- sys is a very standard one
import sys
import time
import random
import math
'''建立電梯'''
class elevator:
    def __init__(self, id, floor , dir , psg):
        self.id=id 
        self.floor = floor #電梯在第幾樓
        self.dir=dir #up,down,stop 
        self.psg=psg #number of people 0~10
    def getIn(self,psg):
        if len(self.psg)<10:
            self.psg.append(psg)
    def getOut(self,psg):
        self.psg.remove(psg)
    def notFull():
        if len(self.psg)<10:
            return True
        else:
            return False
    '''
    def isNotNull():
        if self.psg:
            return True
        else:
            return False
    '''

'''是否還有人在等電梯'''
def waitElevator(pasition):
    for p in pasition:
        if p:
            return True
    return False

'''找最 高 要到幾樓'''
def findMaxFloor(a,b):
    
    tempA = 0
    tempB = 0
    for x in b:
        if x:
            tempB=x[0][0]#等待電梯的人最高樓層       
    if a:
        tempA=max(a,key=lambda item:item[1])[1]#抓乘客抵達樓層最大值
         
    return max(tempA,tempB)

'''找最 低 要到幾樓'''
def findMinFloor(a,b):
    tempA = 0
    tempB = 0
    for x in b:
        if x:
            tempB=x[0][0]#等待電梯的人最高樓層
            break   
    if a:
        tempA=min(a,key=lambda item:item[1])[1]#抓乘客抵達樓層最大值
         
    return min(tempA,tempB)
'''搭電梯'''
def takeElevator(elevator,sumTime,position):
    tempDir=False
    for psg in list(elevator.psg):
        if elevator.floor==psg[1]: # elevator.floor樓有人要離開電梯                                        
            tempDir=True #電梯停不停
            elevator.getOut(psg)#離開電梯
            sumTime+=1#每離開一個人花費一秒
    if position[elevator.floor]: #elevator.floor樓有人要搭電梯
        tempDir=True #電梯停不停 
        for psg in list(position[elevator.floor]): #elevator.floor樓所有乘客
            if len(elevator.psg)<10:#elevator1.notFull: #電梯未滿載
                elevator.getIn(psg)#進入電梯
                position[elevator.floor].remove(psg)#離開樓層
                sumTime+=1#每進入一個人花費一秒
    return tempDir
'''選樓層'''
def whatFloor(elevator,position):
    
    
    f=elevator.floor
    '''1~max~1'''
    if elevator.dir=='up'and f < findMaxFloor(elevator.psg,position): #電梯方向 18:#
        f+=1
    else:
        elevator.dir='down'
    if elevator.dir=='down' and f > findMinFloor(elevator.psg,position): #電梯方向 0:#
        f-=1
    else:
        elevator.dir='up'
    elevator.floor= f

def main():
    #for i in range(100):        
        #a=[179,208,306,93,859,984,55,9,271,33]
        #a=[random.randint(1, 18) for _ in range(10)]#產生10個1~1000的亂數
        #b=[random.randint(1, 18) for _ in range(10)]#產生10個1~1000的亂數
        
        
        '''建立乘客'''
        #a=[(random.randint(1, 18),random.randint(1, 18)) for _ in range(50)]#產生10個1~1000的亂數
        a=[(1, 5), (1, 3), (1, 14), (1, 11), (1, 6), (1, 13), (1, 15), (1, 7), (1, 9), (1, 9), (1, 9), (18, 9), (2, 9)]
        #a=[(17, 5), (11, 3), (13, 8), (5, 16), (18, 16), (3, 6), (7, 1), (2, 1), (6, 13), (18, 8), (15, 9), (1, 8), (9, 12), (7, 3), (13, 6), (9, 10), (4, 6), (17, 16), (17, 14), (13, 16), (18, 10), (12, 18), (18, 8), (2, 4), (3, 1), (17, 13), (9, 11), (6, 9), (17, 3), (7, 14), (15, 10), (7, 1), (2, 16), (3, 16), (4, 2), (3, 4), (4, 7), (8, 2), (14, 18), (1, 10), (10, 5), (3, 15), (15, 9), (9, 2), (16, 7), (18, 11), (1, 16)]	
        
        #去除重複
        for t in a:
            if t[0]== t[1] :
                a.remove(t)
        #print ("*序列",a)
        
        #依照抵達樓層排序
        #a.sort(key=lambda tup: tup[1])
        #print ("*序列",a)
        
        #依照所在樓成排序
        a.sort()
        #print("*序列",a)
        
        position=[[] for i in range(19)]#list[0:18]的二維list
        for t in a:
            position[t[0]].append(t)
        #print (position)#每層樓要搭電梯的人 放在同一層樓
        #建立電梯
        elevator1 =elevator(1,0,'up',[])#等待人數最多的樓層 低往高
        elevator2 =elevator(2,19,'down',[])#等待人數最多的樓層 高往底
        elevator3 =elevator(3,0,'up',[])#抵達相同樓層 人數最多 走訪
        #顯示每層樓要搭電梯的人
        '''for p in position:
            if p:
                print (p)'''
        #計時
        sumTime1=0
        sumTime2=0
        sumTime3=0
        ##1~18樓
        while waitElevator(position) or elevator1.psg or elevator2.psg or elevator3.psg :
            #sumTime+=10 #電梯移動一層樓的時間
                        
            whatFloor(elevator1,position)#移動電梯
            whatFloor(elevator2,position)#移動電梯
            if takeElevator(elevator1,sumTime1,position):#True停 False不停
                sumTime1+=4#電梯開關加啟動煞車時間
                
                print('\nFloor=',elevator1.floor,' 等電梯的人=',position)
                print('\n\televator=1 乘客=',len(elevator1.psg),elevator1.psg)
            if takeElevator(elevator2,sumTime2,position):#True停 False不停
                sumTime2+=4#電梯開關加啟動煞車時間
                print()
                print('\nFloor=',elevator2.floor,' 等電梯的人=',position)
                print('\n\televator=2 乘客=',len(elevator2.psg),elevator2.psg)
                
        print(sumTime1,'\t',sumTime2)
if __name__ == '__main__':
    main()
