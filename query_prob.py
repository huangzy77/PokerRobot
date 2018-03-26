# -*- coding: utf-8 -*-
#查询模块，将main中传来的牌型，查询出相应的胜率
import prob_core
import pickle
from itertools import combinations
#获取所有的牌型
hs=['r','b','f','m']#花色
pz=['1','2','3','4','5','6','7','8','9','10','11','12','13']#牌值
px=[]
for i in hs:
    for j in pz:
        px.append(i+j)
#主函数——概率查询

def query_prob(q_str):#输入一个牌型list，返回胜率float
    q_str_len=len(q_str)
    #起手牌两张的情况,用制作好的dict去找
    if q_str_len==2:
        #读取文件
        f1=open('px_2.pkl','rb')
        px2_data_load=pickle.load(f1)
        f1.close()
        result=px2_data_load.get(tuple(q_str))
        if result==None:
            q_str_temp=[]
            q_str_temp.append(q_str[1])
            q_str_temp.append(q_str[0])           
            result=px2_data_load.get(tuple(q_str_temp))
        return result
    #开开三张牌后的概率，现在已知道5张牌了，另外2两张用循环得到
    if q_str_len==5:
        px_5remove=[]
        for k in px:#这才能初始化
            px_5remove.append(k)
        temp_q_str=[]#开新内存，保持固定不动
        for data in q_str:
            temp_q_str.append(data)
        for l in temp_q_str:
            px_5remove.remove(l)#获取去掉已有那2张牌型后，剩下的50张扑克牌
        px_5remove_comb=combinations(px_5remove,2)#将剩下的50张扑克牌50选5后，加上原来的两张，组合成7张牌的组合
        temp5=0
        kn5=1081#52-5=47,47选2的组合数
        for qs2 in px_5remove_comb:
            quary_px=q_str+list(qs2)
            temp5=temp5+prob_core.prob_victory(quary_px)
        return float(temp5)/float(kn5)
    #开开四张牌后的概率，现在已知道6张牌了，另外1两张用循环得到
    if q_str_len==6:
        px_6remove=[]
        for k in px:#这才能初始化
            px_6remove.append(k)
        for i6 in q_str:
            px_6remove.remove(i6)#获取去掉已有那6张牌型后，剩下的46张扑克牌
        temp6=0
        kn6=46#52-6=46
        for qs1 in px_6remove:
            temp_q_str=q_str+[qs1]
            temp6=temp6+prob_core.prob_victory(temp_q_str)
        return float(temp6)/float(kn6)
    #开开7张牌后的概率
    if q_str_len==7:
        return prob_core.prob_victory(q_str)
  
def query_prob2(q_str_sp,q_str_kp):#输入一个牌型list，返回胜率float
    q_str_kp_len=len(q_str_kp)
    px_2=list(combinations(px,2))
    px_2_num=len(px_2)
    #起手牌两张的情况,用制作好的dict去找
    if q_str_kp_len==0:
        temp0=0
        temp_query_2=q_str_sp
        p_sp_0=query_prob(temp_query_2)
        #计算起手两张牌所有的牌型组合
        for px2_0 in px_2:
            temp_query_3_other=px2_0
            if query_prob(temp_query_3_other)<p_sp_0:
                temp0=temp0+1
        return float(temp0)/float(px_2_num)
    #开开三张牌后的概率，现在已知道5张牌了，另外2两张用循环得到
    if q_str_kp_len==3:
        temp3=0
        temp_query_5=q_str_kp+q_str_sp
        p_sp_3=query_prob(temp_query_5)
        try:
            px_2_remove_sp=px_2.remove(tuple(q_str_sp))
        except Exception,e:
            q_temp=[]
            q_temp.append(q_str_sp[1])
            q_temp.append(q_str_sp[0])
            px_2.remove(tuple(q_temp))     
        #计算起手两张牌所有的牌型组合
        for px2_3 in px_2:
            temp_query_5_other=q_str_kp+list(px2_3)
            
            print temp_query_5_other            
            if query_prob(temp_query_5_other)<p_sp_3:
                temp3=temp3+1 
        return temp3/px_2_num
    #开开四张牌后的概率，现在已知道6张牌了，另外1两张用循环得到
    if q_str_len==4:
        temp4=0
        temp_query_6=q_str_kp+q_str_sp
        p_sp_4=query_prob(temp_query_6)
        #计算起手两张牌所有的牌型组合
        for px2_4 in px_2:
            temp_query_6_other=q_str_kp+lsit(px2_4)
            if query_prob(temp_query_6_other)<p_sp_4:
                temp4=temp4+1
        return temp4/px_2_num
    #开开5张牌后的概率
    if q_str_len==5:
        temp5=0
        temp_query_7=q_str_kp+q_str_sp
        p_sp_5=query_prob(temp_query_7)
        #计算起手两张牌所有的牌型组合
        for px2_5 in px_2:
            temp_query_7_other=q_str_kp+list(px2_5)
            if query_prob(temp_query_7_other)<p_sp_5:
                temp5=temp5+1
        return temp5/px_2_num
    
            
#ttemp=['m7', 'f9', 'm12', 'b8', 'r12', 'm4', 'r13']  
#print qurery_prob(ttemp)
#q_str_sp=['m7', 'f9']
#q_str_kp=['m12', 'b8', 'r12'] 
#print query_prob2(q_str_sp, q_str_kp)     
        