# -*- coding: utf-8 -*-
#功能描述：prob_core()该函数模块，输入组合，输出输的概率，即前面有多少比它大的组合
from collections import Counter
from wheel.signatures.djbec import double


#用到的常量

#函数区域

#分离出7牌组合的花色和牌型
def separate_zh(zh):
    poker_hs=[]#花色str
    poker_pz=[]#牌值int
    for num in range(7):       
        poker_hs.append(zh[num][0])
        poker_pz.append(int(zh[num].replace(zh[num][0], '')))
    return poker_hs,poker_pz

#辅助函数——将传入的字符串分类(输入7张牌的组合，输出类别str)
def prob_classify(zh):
    flag=0#用于存储牌型的字符串，1-10,分别为皇家同花顺到高牌
    #将传入的list，分割成7张牌的花色和牌值
    poker_hs,poker_pz=separate_zh(zh)
    #下面开始分类，采用层层过滤的方式
    #第一类皇家同花顺，是否是同花，是否是顺子，最大值为A
    bo_ths,ths_max=is_ths(zh)
    if bo_ths and ths_max==14:
        flag=1
        return flag
    #第二类为同花顺
    if bo_ths and ths_max<14:
        flag=2
        return flag
    #第三类为四条，连续值判断排名第一的是4
    if num_sort(poker_pz)[0][2]==4:
        flag=3
        return flag
    #第四类为葫芦，连续值判断排名第一的是3,第二的大于1
    if num_sort(poker_pz)[0][2]==3 and num_sort(poker_pz)[1][2]>1:
        flag=4
        return flag
    #第五类为同花
    bo,hs=is_sameColor(poker_hs)
    if bo:
        flag=5
        return flag
    #第六类为顺子
    if is_straight(poker_pz)[0]==1:
        flag=6
        return flag
    #第七类为三条，连续值排名第一的是3,第二的是1
    if num_sort(poker_pz)[0][2]==3 and num_sort(poker_pz)[1][2]==1:
        flag=7
        return flag
    #第八类为两对，连续值排名第一的是2,第二的是2
    if num_sort(poker_pz)[0][2]==2 and num_sort(poker_pz)[1][2]==2:
        flag=8
        return flag
    #第九类为对子，连续排名第一的是2,第二的是1
    if num_sort(poker_pz)[0][2]==2 and num_sort(poker_pz)[1][2]==1:
        flag=9
        return flag
    #第十类为高牌
    else:
        flag=10
    return flag   
#辅助函数——判断是否为同花（输入花色list,输出是否为同花bool）
def is_sameColor(poker_hs):
    c=Counter(poker_hs)#数出个数
    if c['f']>=5 :return True,'f'
    if c['m']>=5 :return True,'m'
    if c['r']>=5 :return True,'r'
    if c['b']>=5 :return True,'b'
    return False,''
#辅助函数——判断是否是顺子及顺子中的最大值（输入牌值list，输出list包括是否为顺子（1为是，0为否），并且返回最大值）
def is_straight(poker_pz):
    if 1 in poker_pz:
        for i in range(len(poker_pz)):
            if poker_pz[i]==1:
                poker_pz[i]=14
        if is_straight_sub(poker_pz)[0]==0:#如果A在后面没有链上，那就试试前面
            for i in range(len(poker_pz)):
                if poker_pz[i]==14:
                    poker_pz[i]=1        
    return is_straight_sub(poker_pz)

def is_straight_sub(poker_pz):#注意！还有含有A的情况
    result=[0,0]
    pz_sort=sorted(poker_pz)#排序
    pz_sort=list(set(pz_sort))#去掉重复的数
    for i in range(len(pz_sort)-4):#排序后，从小到大，看有没有可能形成5联
        temp=0
        for j in range(4):
            if pz_sort[i+j+1]-pz_sort[i+j]==1:
                temp=temp+1
            if temp==4:
                result[0]=1
                result[1]=pz_sort[i+j+1]
    return result   
#辅助函数——有多少相同的牌，输出list,同牌数排名\牌值\同牌数
def num_sort(poker_pz):
    c_num=Counter(poker_pz)#数出每个牌值的数量
    c_num_sorted=sorted(c_num.items(), key=lambda d: d[1],reverse=True)#同牌数从大到小的排序
    #将排序写入返回的list
    result=[]
    for i in range(len(c_num_sorted)):
        result.append([i,c_num_sorted[i][0],c_num_sorted[i][1]])
    return result
#辅助函数——专门用来判断同花顺的
def is_ths(zh):
    poker_hs,poker_pz=separate_zh(zh)
    bo,hs=is_sameColor(poker_hs)#获取是否是同花和同花的花色
    if bo:
        #同花花色的牌值有哪些index,记录下来,然后看这些index下的数是不是顺子
        pz_th=[]
        for i in range(len(zh)):
            if poker_hs[i]==hs:
                pz_th.append(poker_pz[i])      
        if is_straight(pz_th)[0]==1:#同花里面有顺子就行了
            return True,is_straight(pz_th)[1]      
    return False,0
    
#核心函数——查询7张牌的胜率，输入list,返回float
def prob_victory(q_7):#查询7张牌的胜率，输入list,返回float
    poker_hs,poker_pz=separate_zh(q_7)
    vic=0
    #记录10种牌型的牌型数(caculate_howManykidsinClasses)
    '''
    bef_base0=0
    bef_base1=4324
    bef_base2=37260
    bef_base3=224848
    bef_base4=3473184
    bef_base5=4047644
    bef_base6=6180020
    bef_base7=6461620
    bef_base8=31433400
    bef_base9=58627800
    bef_base10=23294460
    all_prob=133784560 #52选7,所有的组合数
    '''
    bef_base0=0
    bef_base1=4324
    bef_base2=25404
    bef_base3=224848
    bef_base4=3473184
    bef_base5=4059500
    bef_base6=6069060
    bef_base7=6481860
    bef_base8=31524120
    bef_base9=58627800
    bef_base10=23294460
    all_prob=133784560 #52选7,所有的组合数
    #首先将q_7分类,类别为int
    lb=prob_classify(q_7)
    if lb==1:#如果是皇家同花顺组合之前的数目为0
        inside_index1=0
        bef=bef_base0+inside_index1
    if lb==2:#此顺子A就是1,不用换,后面计算时就不要减去1
        data2=is_straight(poker_pz)[1]#顺子中的最大值
        #顺子一共10个格子，5-A
        inside_index2=(10-(data2-4))*(bef_base2/10)#格子总数-（排序的值-最小的值+1）就是前面有几格，乘以每个格子大小，就是你前面的数。反正格子是均分的
        bef=bef_base0+bef_base1+inside_index2
    if lb==3:
        for i3 in range(len(poker_pz)):#不牵涉顺子问题，把1全部换为A,方便后面的比较运算
            if poker_pz[i3]==1:
                poker_pz[i3]=14 
        data3=num_sort(poker_pz)           
        data4_value=data3[0][1]
        data_no4=poker_pz
        for j3 in range(4):#把4链子去点，找出最大的那个
            data_no4.remove(data4_value)
        data_no4_max=max(data_no4)
        inside_index3=(13-(data4_value-1))*(bef_base3/13)+(11-(data_no4_max-2))*bef_base3/13/11
        bef=bef_base0+bef_base1+bef_base2+inside_index3
    if lb==4:
        for i4 in range(len(poker_pz)):#不牵涉顺子前链接问题，把1全部换为A,方便后面的比较运算
            if poker_pz[i4]==1:
                poker_pz[i4]=14
        data4=num_sort(poker_pz)
        data3_value=data4[0][1]
        data2_value=data4[1][1]
        inside_index4=(13-(data3_value-1))*(bef_base4/13)+(11-(data2_value-2))*(bef_base4/13/11)
        bef=bef_base0+bef_base1+bef_base2+bef_base3+inside_index4
    if lb==5:
        for i4 in range(len(poker_pz)):#不牵涉顺子前链接问题，把1全部换为A,方便后面的比较运算
            if poker_pz[i4]==1:
                poker_pz[i4]=14
        bo,hs=is_sameColor(poker_hs)#获取是否是同花和同花的花色
        pz_th=[]#记录下这些同花的牌值
        for i in range(len(q_7)):
            if poker_hs[i]==hs:
                pz_th.append(poker_pz[i])
        pz_th_sorted=sorted(pz_th,reverse=True)#形成最大的同花开始算
        inside_index5=(14-pz_th_sorted[0])*(bef_base5/8)+(13-pz_th_sorted[1])*(bef_base5/8/9)+(12-pz_th_sorted[2])*(bef_base5/8/9/9)+(11-pz_th_sorted[3])*(bef_base5/8/9/9/9)\
        +(9-pz_th_sorted[4])*(bef_base5/8/9/9/9/8)
        bef=bef_base0+bef_base1+bef_base2+bef_base3+bef_base4+inside_index5
    if lb==6:
        data6=is_straight(poker_pz)[1]#顺子中的最大值
        #顺子一共10个格子，5-A
        inside_index6=(10-(data6-4))*(bef_base6/10)#格子总数-（排序的值-最小的值+1）就是前面有几格，乘以每个格子大小，就是你前面的数。反正格子是均分的
        bef=bef_base0+bef_base1+bef_base2+bef_base3+bef_base4+bef_base5+inside_index6
    if lb==7:
        for i7 in range(len(poker_pz)):#不牵涉顺子问题，把1全部换为A,方便后面的比较运算
            if poker_pz[i7]==1:
                poker_pz[i7]=14 
        data7=num_sort(poker_pz)           
        data7_value=data7[0][1]
        data_no3=poker_pz
        for j7 in range(3):#把4链子去掉，循环3次remove,找出最大的那个
            data_no3.remove(data7_value)
        data_no3_sorted=sorted(data_no3,reverse=True)
        inside_index7=((13-(data7_value-1))*(bef_base7/13))+((11-(data_no3_sorted[0]-2))*bef_base7/13/11)+((9-(data_no3_sorted[1]-3))*bef_base7/13/11/9)
        bef=bef_base0+bef_base1+bef_base2+bef_base3+bef_base4+bef_base5+bef_base6+inside_index7
    if lb==8:#两对有三个数进入格子
        for i7 in range(len(poker_pz)):#不牵涉顺子问题，把1全部换为A,方便后面的比较运算
            if poker_pz[i7]==1:
                poker_pz[i7]=14
        data8=num_sort(poker_pz)
        if data8[0][1]>data8[1][1]:
            data8_1=data8[0][1]
            data8_2=data8[1][1]
        else:
            data8_2=data8[0][1]
            data8_1=data8[1][1]
        data8_noDouble=poker_pz
        for i8 in range(2):
            data8_noDouble.remove(data8_1)
            data8_noDouble.remove(data8_2)
        data8_3=max(data8_noDouble)
        inside_index8=((13-(data8_1-1))*(bef_base8/13))+((11-(data8_2-2))*bef_base8/13/11)+((9-(data8_3-3))*bef_base8/13/11/9)
        bef=bef_base0+bef_base1+bef_base2+bef_base3+bef_base4+bef_base5+bef_base6+bef_base7+inside_index8  
    if lb==9:
        for i7 in range(len(poker_pz)):#不牵涉顺子问题，把1全部换为A,方便后面的比较运算
            if poker_pz[i7]==1:
                poker_pz[i7]=14
        data9=num_sort(poker_pz)
        data9_double_value=data9[0][1]
        data9_noDouble=poker_pz
        for i9 in range(2):
            data9_noDouble.remove(data9_double_value)
        data9_noDouble_sorted=sorted(data9_noDouble,reverse=True)
        inside_index9=((13-(data9_double_value-1))*(bef_base9/13))+((11-(data9_noDouble_sorted[0]-2))*bef_base9/13/11)+((9-(data9_noDouble_sorted[1]-3))*bef_base9/13/11/9)\
        +((7-(data9_noDouble_sorted[2]-4))*bef_base9/13/11/9/7)
        bef=bef_base0+bef_base1+bef_base2+bef_base3+bef_base4+bef_base5+bef_base6+bef_base7+bef_base8+inside_index9
    if lb==10:
        for i7 in range(len(poker_pz)):#不牵涉顺子问题，把1全部换为A,方便后面的比较运算
            if poker_pz[i7]==1:
                poker_pz[i7]=14
        data10=sorted(poker_pz,reverse=True)
        inside_index10=((13-(data10[0]-1))*(bef_base10/13))+((11-(data10[1]-2))*bef_base10/13/11)+((9-(data10[2]-3))*bef_base10/13/11/9)\
        +((7-(data10[3]-4))*bef_base10/13/11/9/7)+((5-(data10[3]-5))*bef_base10/13/11/9/7/5)
        bef=bef_base0+bef_base1+bef_base2+bef_base3+bef_base4+bef_base5+bef_base6+bef_base7+bef_base8+bef_base9+inside_index10
    #通过前面组合数bef计算出胜率
    vic=1-float(bef)/float(all_prob)                
    #注意每种组合进行最大组合和最小组合测试啊，看看bef值正确否
    return vic

#tempp=['r1', 'b1', 'r2', 'b4', 'r5','m3','r13']
#测试用list
#print prob_victory(tempp)
#print prob_classify(tempp)
