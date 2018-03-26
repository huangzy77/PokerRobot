# -*- coding: utf-8 -*-
#用于暴力计算每种分类中的个数
import prob_core
from itertools import combinations

#用到的常量
hs=['r','b','f','m']#花色
pz=['1','2','3','4','5','6','7','8','9','10','11','12','13']#牌值

#计算所有的牌型
px=[]
for i in hs:
    for j in pz:
        px.append(i+j)

#组合出52选7所有组合，记录分类
t1=t2=t3=t4=t5=t6=t7=t8=t9=t10=t11=0 #记录每种分类的个数
num=0 #记录总数
temp=0#记录类型
for k in combinations(px,7):
    temp=prob_core.prob_classify(k)
    if temp==1:t1=t1+1
    else :
        if temp==2:t2=t2+1
        else:
            if temp==3:t3=t3+1
            else:
                if temp==4:t4=t4+1
                else:
                    if temp==5:t5=t5+1
                    else:
                        if temp==6:t6=t6+1
                        else:
                            if temp==7:t7=t7+1
                            else:
                                if temp==8:t8=t8+1
                                else:
                                    if temp==9:t9=t9+1
                                    else:
                                        if temp==10:t10=t10+1
                                        else: 
                                            t11=t11+1
                                            print "Oh,no!"
    num=num+1
    print num,':',k,temp
    print 't1:',t1,' ','t2:',t2,' ','t3:',t3,' ','t4:',t4,' ','t5:',t5,' ','t6:',t6,' ','t7:',t7,' ','t8:',t8,' ','t9:',t9,' ','t10:',t10,'t11:',t11
    

    
