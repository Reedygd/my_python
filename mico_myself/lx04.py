import os
import re
import time
from matplotlib import pyplot as plt
from matplotlib import animation
import numpy as np


def getTotalPss(process_name):
    lines = os.popen("adb shell dumpsys meminfo %s " % process_name).readlines() #逐行读取
    total = "TOTAL"
    for line in lines:
        if re.findall(total, line):
            lis = line.split(" ")
            while '' in lis:
                lis.remove('')
            return int(lis[1])/1024 #返回总共内存使用

def getTotalFree():
    '''获取总的空闲内存'''
    lines = os.popen("adb shell free -h ").readlines()
    for line in lines:
        if re.findall("Mem:",line):
            lis = line.split(" ")
            while '' in lis:
                lis.remove('')
            return lis[3].strip('M')

def getCpu():
    li = os.popen('adb shell " top -n 1 -s 10 "').readlines()
    name = "com.xiaomi.mico+"
    for line in li:
        if re.findall(name,line):
            print('okok')
            cuplist = line.split(" ")
            #print(cuplist)
            if cuplist[-1].strip() == 'com.xiaomi.mico+':
                #print(cuplist)
                while '' in cuplist:       # 将list中的空元素删除
                    cuplist.remove('')
                return float(cuplist[-3].strip('%')) #去掉百分号，返回一个float


def main(count):
    plt.figure()
    x=[]
    y=[]
    i=0
    f1=open("E:\\my project\\123.txt",'w')
    f2=open("E:\\my project\\totalfree.txt",'w')
    while i<count:
        f1.write(str(i)+','+str(getTotalPss())+'\n')
        f2.write(str(i)+','+getTotalFree()+'\n')
        i+=1
        time.sleep(120)
    f1.close()
    f2.close()
    x, y1 = np.loadtxt('E:\\my project\\123.txt', delimiter=',', unpack=True)
    x, y2 = np.loadtxt('E:\\my project\\totalfree.txt', delimiter=',', unpack=True)
    plt.plot(x, y1, label='total pss')
    plt.plot(x, y2, label='total free')
    plt.yticks((0,15,30,50,60,70,80,100,120,150))
    plt.xlabel("x:count")
    plt.ylabel("y:mem(Mbytes)")
    plt.grid(linestyle='--')
    plt.legend()
    plt.show()
if __name__ =='__main__':
    main(300)
