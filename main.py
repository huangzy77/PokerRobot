# -*- coding: utf-8 -*-
import query_prob
from IN import IN_CLASSA_MAX
#变量定义
sp2_str=''#两张手牌，以空格为间隔

#欢迎词和说明
print "欢迎使用德州扑克无敌手！(按qq为推出)"
print '游戏开始了！'


#辅助函数——凯利公式
def kaly(probvic,probloss,probwin):#凯利公式，赢率、可能输的钱金额,返回可投入总仓位的比例    
    b=float(probwin)/float(probloss)
    p=float(probvic)
    q=1-p
    f=float(b*p-q)/b
    return f
#辅助函数——回答是否跟或者加
def Myanswer(allmoney,costmoney,getmoney,q_px):#输入三个整数，一个查询list，输出一个字符串回答问题
    probvic=query_prob.qurery_prob(q_px)#查询这个牌型的胜率
    f=kaly(probvic, costmoney, getmoney)#
    betMoney=allmoney*f#按照凯利公式算出的下注值
    if betMoney>=costmoney:
        return answer_sub_isMore(betMoney, costmoney, getmoney, probvic)
    else:
        return "让或者弃了吧！"
    
def answer_sub_isMore(betMoney,costmoney,getmoney,probvic): #按照凯利公式应该下的注，直接跟付出的钱，赢的钱，胜率
    if betMoney>=costmoney*2:
        f=kaly(probvic, betMoney, getmoney)
        if f>0:
            return "加注1倍" 
        else:
            return "跟！" 
    else:
        return '跟！' 
     
     

   
#进入主循环
'''
sp=[]#记录手牌
jzp=0#记录现在有几张牌
cost_total=0#记录已经下了多少注了
AllMoney_int=int(raw_input('您有多少筹码：（手里总共的钱）')) 
while(jzp<=7):#推出就输入一个牌数大于7的数字   
    jzp=int(raw_input('现在您看到几张牌？'))
    if jzp==2:
        if len(sp)<2:
            sp2_str=raw_input('您看到的两张手牌是什么？（以空格间隔）')
            sp=sp2_str.split(' ')
        print '您看到的牌型是： ',sp
        CostMoney_int=int(raw_input("您需要付出多少（跟需要多少钱）"))
        GetMoney_int=int(raw_input("您你能挣到多少（现在的底注）"))
        print Myanswer(AllMoney_int-cost_total,CostMoney_int,GetMoney_int,sp)
        cost_total=cost_total+CostMoney_int
        continue
    if jzp==5:
        if len(sp)<5:
            sp3_str=raw_input('新开出来的3张牌是啥？（以空格间隔）')
            sp3=sp3_str.split(' ')
            sp=sp+sp3
        print '您看到的牌型是： ',sp
        CostMoney_int=int(raw_input("您需要付出多少（跟需要多少钱）"))
        GetMoney_int=int(raw_input("您你能挣到多少（现在的底注）"))
        print Myanswer(AllMoney_int-cost_total,CostMoney_int,GetMoney_int,sp)
        cost_total=cost_total+CostMoney_int
        continue
    if jzp==6:
        if len(sp)<6:
            sp6_str=raw_input('新开出来的1张牌是啥？')
            sp6=[sp6_str]
            sp=sp+sp6
        print '您看到的牌型是： ',sp
        CostMoney_int=int(raw_input("您需要付出多少（跟需要多少钱）"))
        GetMoney_int=int(raw_input("您你能挣到多少（现在的底注）"))
        print Myanswer(AllMoney_int-cost_total,CostMoney_int,GetMoney_int,sp)
        cost_total=cost_total+CostMoney_int
        continue
    if jzp==7:
        if len(sp)<7:
            sp7_str=raw_input('新开出来的1张牌是啥？')
            sp7=[sp7_str]
            sp=sp+sp7
        print '您看到的牌型是： ',sp
        CostMoney_int=int(raw_input("您需要付出多少（跟需要多少钱）"))
        GetMoney_int=int(raw_input("您你能挣到多少（现在的底注）"))
        print Myanswer(AllMoney_int-cost_total,CostMoney_int,GetMoney_int,sp)
        cost_total=cost_total+CostMoney_int
        continue
    else:
        print '新牌局开始！'   
        sp=[] 
        jzp=0
        cost_total=0
'''
#辅助函数——输入判断输入字符串的含义
def input_mean(str):#输入字符串
    global temp_dz,temp_gz,sp#global 用法很重要，申明过后才能使用全局变量
    str_first=str[0]
    if str_first=='g':#有人跟注的情况
        temp_dz=temp_dz+temp_gz
        return "有人跟了%d"%(temp_gz)+" 现在底注有%d"%(temp_dz)
    if str_first=='j':#有人加注的情况
        j_int=int(str[1:])
        temp_gz=j_int
        temp_dz=temp_dz+temp_gz
        return "有人加注%d"%(j_int)+" 现在的底注有%d"%(temp_dz)
    if str_first=='k':#开牌的情况
        pz_str=str[2:]
        pz_l=pz_str.split(' ')
        #把jqka,改为11,12,13,1
        for i in range(len(pz_l)):
            if pz_l[i][1]=='a':pz_l[i]=pz_l[i].replace('a','1')
            if pz_l[i][1]=='j':pz_l[i]=pz_l[i].replace('j','11')
            if pz_l[i][1]=='q':pz_l[i]=pz_l[i].replace('q','12')
            if pz_l[i][1]=='k':pz_l[i]=pz_l[i].replace('k','13')
        sp=sp+pz_l   
        return "Your poker is: ",sp
    if str_first=='w':#询问我应该怎么办
        allmoney=int(str[1:])
        return Myanswer(allmoney, temp_gz, temp_dz, sp)
    if str_first=='a':#有人allin
        a_m=int(str[1:])#allin的金额
        if a_m>temp_gz:
            temp_gz=a_m
            temp_dz=temp_dz+temp_gz
        else:
            temp_dz=temp_dz+temp_gz
        return "有人allin了%d"%(a_m)
    if str_first=='q':#新的一局开始
        temp_dz=0#用于存储底注
        temp_gz=0#用于存储跟注需要的金额
        sp=[]#用于存储手牌
        mz_str=raw_input('盲注多少？')
        mz_int=int(mz_str) 
        temp_dz=mz_int*1.5#初始化
        temp_gz=mz_int
        return "新的一局开始"
    else:
        return"打错了，重新打！"
        
    
        
'''   
#进入主流程。说明：g有人跟，j123有人加注123，a123有人allin123,w2000为询问我应该干啥子我手里的钱，k b10 fq m9为开出三张牌,q为退出开新局
temp_dz=0#用于存储底注
temp_gz=0#用于存储跟注需要的金额
sp=[]#用于存储手牌
mz_str=raw_input('盲注多少？')
mz_int=int(mz_str) 
temp_dz=mz_int*1.5#初始化
temp_gz=mz_int
input_str=''
while(1):#q为退出
    input_str=raw_input("现在的情况是：")
    print input_mean(input_str)
    
'''
        



    
        
    
    