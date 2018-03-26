# -*- coding: utf-8 -*-
#用于暴力计算起手胜率表的问题，输出一个字典，并保存为HDF5文件

import prob_core
from itertools import combinations
import pickle #写入文件使将字典序列化和读取时反序列化


#用到的常量
hs=['r','b','f','m']#花色
pz=['1','2','3','4','5','6','7','8','9','10','11','12','13']#牌值
kn=2118760#50选5的组合数，就是每个起手对背后可能存在的组合
#计算所有的牌型
px=[]
for i in hs:
    for j in pz:
        px.append(i+j)
#计算起手两张牌所有的牌型组合
px_2=list(combinations(px,2))
#遍历每一种起手牌型组合,得到每种牌型组合的概率,并将其存入字典，牌型组合为index,牌型组合的胜率为value
result={}
for qs2 in px_2:
    print len(result)
    temp=0
    px_2remove=[]
    for k in px:#这才能初始化,开辟新内存
        px_2remove.append(k)
    #px_2remove=px#只是传递了地址，px_2remove改变，px跟着改变了
    px_2remove.remove(qs2[0])#获取去掉已有那2张牌型后，剩下的50张扑克牌
    px_2remove.remove(qs2[1])
    px_2remove_comb=combinations(px_2remove,5)#将剩下的50张扑克牌50选5后，加上原来的两张，组合成7张牌的组合
    for qs5 in px_2remove_comb:
        quary_px=qs2+qs5
        temp=temp+prob_core.prob_victory(quary_px)
    result[qs2]=float(temp)/float(kn)
    print result

#输出result到文件，使用pickle
f=open('px_2.pkl','wb')
byte_data=pickle.dump(result,f,True)
f.close()

#读取文件
f1=open('px_2.pkl','rb')
px2_data_load=pickle.load(f1)
f1.close()
print px2_data_read
    
