#-*-encoding:utf-8-*-
from PIL import Image
import image_p.image_pre
from os import popen,getcwd,mkdir
from image_p import image_pre,image_re
from time import sleep
import query_prob
from _locale import AM_STR

#辅助函数--规定动作
def do_main(flag):#根据输入的字符串作出动作
    if flag==1:
        popen('adb shell input tap 900 680')
        sleep(0.5)
        return 0
    if flag==0:
        popen('adb shell input tap 620 680')
        sleep(0.5)
        return 0 
    if flag==2:
        popen('adb shell input tap 1150 680')
        sleep(0.1)
        popen('adb shell input tap 1170 343')
        sleep(0.1)
        popen('adb shell input tap 1150 680')
        sleep(0.1)
        popen('adb shell input tap 900 680')
        sleep(0.1)
        return 0
    else:
        popen('adb shell input tap 620 680')
        sleep(0.5)
        return 0

#辅助函数--将识别出的扑克数字，转换为扑克花色和牌值
def poker_c(pre_num):#输入int，返回str
    pre_str=str(pre_num)
    if pre_str[0]=='1':
        re_poker='r'+pre_str[1:]
    if pre_str[0]=='2':
        re_poker='b'+pre_str[1:]
    if pre_str[0]=='3':
        re_poker='m'+pre_str[1:]
    if pre_str[0]=='4':
        re_poker='f'+pre_str[1:]
    return re_poker
#辅助函数——凯利公式
def kaly(probvic,probloss,probwin):#凯利公式，赢率、可能输的钱金额,返回可投入总仓位的比例    
    b=float(probwin)/float(probloss)
    p=float(probvic)
    q=1-p
    f=float(b*p-q)/b
    return f
#辅助函数——回答是否跟或者加
def Myanswer(allmoney,costmoney,getmoney,q_px,str_zt):#输入三个整数，一个查询list，输出一个字符串回答问题         
    global ksz_int
    probvic=query_prob.query_prob(q_px)#查询这个牌型的胜率
    print probvic
    f=kaly(probvic, costmoney, getmoney)#
    print f
    betMoney=ksz_int*f#按照凯利公式算出的下注值
    #在有f betMoney probvic 三个指标可以组合
    if len(q_px)==2:#开手牌，未开牌
        if (f>0 and probvic>0.53):#(f>0 and probvic>0.52 and betMoney>costmoney) or (allmoney==costmoney and probvic>0.52 and f>0):#因为每一局最多翻倍，所以必须大于0.5
            return answer_sub_isMore(betMoney, costmoney, getmoney, probvic,str_zt,q_px)
        else:
            if str_zt==u'让':
                return "让",1
            else:
                return "弃",0 
    if len(q_px)==5:#开三张
        if (f>0 and probvic>0.58):#(f>0 and probvic>0.52 and betMoney>costmoney) or (allmoney==costmoney and probvic>0.52 and f>0):#因为每一局最多翻倍，所以必须大于0.5
            return answer_sub_isMore(betMoney, costmoney, getmoney, probvic,str_zt,q_px)
        else:
            if str_zt==u'让':
                return "让",1
            else:
                return "弃",0
    if len(q_px)==6:#开四张
        if (f>0 and probvic>0.68):#(f>0 and probvic>0.52 and betMoney>costmoney) or (allmoney==costmoney and probvic>0.52 and f>0):#因为每一局最多翻倍，所以必须大于0.5
            return answer_sub_isMore(betMoney, costmoney, getmoney, probvic,str_zt,q_px)
        else:
            if str_zt==u'让':
                return "让",1
            else:
                return "弃",0 
    if len(q_px)==7:#全开完
        if (f>0 and probvic>0.78):#(f>0 and probvic>0.52 and betMoney>costmoney) or (allmoney==costmoney and probvic>0.52 and f>0):#因为每一局最多翻倍，所以必须大于0.5
            return answer_sub_isMore(betMoney, costmoney, getmoney, probvic,str_zt,q_px)
        else:
            if str_zt==u'让':
                return "让",1
            else:
                return "弃",0   
    
def answer_sub_isMore(betMoney,costmoney,getmoney,probvic,str_zt,q_px): #按照凯利公式应该下的注，直接跟付出的钱，赢的钱，胜率
    #加注策略还有待讨论
    if len(q_px)==2 and probvic>0.68:
        return '加',2
    if len(q_px)==5 and probvic>0.78:
        return '加',2
    if len(q_px)==6 and probvic>0.88:
        return '加',2
    if len(q_px)==7 and probvic>0.98:
        return '加',2
    else:
        return '跟/让',1 

#辅助函数，记录图片和识别结果
counter_flag=0
def Myrecord(allmoney, costmoney, getmoney, query_list,str_zt):#输入剪切下的图片，和识别出的结果。将输入存储成文件
    global counter_flag
    mkdir(getcwd()+'/record/'+str(counter_flag))#造文件夹
    im_temp=Image.open(getcwd()+'/pk1_co.png', mode='r')#打开图片并保持
    im_temp.save(getcwd()+'/record/'+str(counter_flag)+'/pk1_co.png')
    im_temp=Image.open(getcwd()+'/pk2_co.png', mode='r')#打开图片并保持
    im_temp.save(getcwd()+'/record/'+str(counter_flag)+'/pk2_co.png')
    im_temp=Image.open(getcwd()+'/pk3_co.png', mode='r')#打开图片并保持
    im_temp.save(getcwd()+'/record/'+str(counter_flag)+'/pk3_co.png')
    im_temp=Image.open(getcwd()+'/pk4_co.png', mode='r')#打开图片并保持
    im_temp.save(getcwd()+'/record/'+str(counter_flag)+'/pk4_co.png')
    im_temp=Image.open(getcwd()+'/pk5_co.png', mode='r')#打开图片并保持
    im_temp.save(getcwd()+'/record/'+str(counter_flag)+'/pk5_co.png')
    im_temp=Image.open(getcwd()+'/ps1_co.png', mode='r')#打开图片并保持
    im_temp.save(getcwd()+'/record/'+str(counter_flag)+'/ps1_co.png')
    im_temp=Image.open(getcwd()+'/ps2_co.png', mode='r')#打开图片并保持
    im_temp.save(getcwd()+'/record/'+str(counter_flag)+'/ps2_co.png')
    im_temp=Image.open(getcwd()+'/zt_co.png', mode='r')#打开图片并保持
    im_temp.save(getcwd()+'/record/'+str(counter_flag)+'/zt_co.png')
    im_temp=Image.open(getcwd()+'/dz_co.png', mode='r')#打开图片并保持
    im_temp.save(getcwd()+'/record/'+str(counter_flag)+'/dz_co.png')
    im_temp=Image.open(getcwd()+'/am_co.png', mode='r')#打开图片并保持
    im_temp.save(getcwd()+'/record/'+str(counter_flag)+'/am_co.png')
    #将识别结果str，然后保存
    s_temp='am:'+str(allmoney)+','+'costmoney:'+str(costmoney)+','+'getmoney:'+str(getmoney)+','+','.join(query_list)
    f=open(getcwd()+'/record/'+str(counter_flag)+'/re.txt','w')
    f.write(s_temp)
    f.close()
    counter_flag=counter_flag+1

#主要循环
print '连接手机，并打开adb模式'
mz=image_re.get_mz()
ksz=raw_input('开始的底注是多少？')
ksz_int=int(ksz)
while(1):
    #获取规定的图像,并存储在当前文件夹
    popen('adb shell screencap -p /sdcard/phone_temp.png')#截图
    popen('adb pull /sdcard/phone_temp.png '+getcwd())#推送到计算机
    im=Image.open(getcwd()+'/phone_temp.png')#计算机图片加载图片到内存
    w,h=im.size#获取分辨率
    image_pre.cut_img(im,getcwd(),w,h)#分割并存储图片
    #利用颜色识别状态
    zt=image_re.get_colornum(getcwd()+'/zt_co.png',(8,8))
    query_list=[]
    print '按钮颜色：',zt[0]
    if zt[0]>85 and zt[0]<93:
        #识别手牌，返回的是int
        ps1=image_re.poker_predict(getcwd()+'/ps1_co.png',getcwd()+'/image_p/net_ps.pkl')
        ps2=image_re.poker_predict(getcwd()+'/ps2_co.png',getcwd()+'/image_p/net_ps.pkl')
        query_list.append(poker_c(ps1))
        query_list.append(poker_c(ps2))
        #判断翻出了几张牌了，读出牌值,形成list
        pk1_color=image_re.get_colornum(getcwd()+'/pk1_co.png',(8,118))
        pk2_color=image_re.get_colornum(getcwd()+'/pk2_co.png',(8,118))
        pk3_color=image_re.get_colornum(getcwd()+'/pk3_co.png',(8,118))
        pk4_color=image_re.get_colornum(getcwd()+'/pk4_co.png',(8,118))
        pk5_color=image_re.get_colornum(getcwd()+'/pk5_co.png',(8,118))
        if pk1_color[0]==238:
            pk1=image_re.poker_predict(getcwd()+'/pk1_co.png',getcwd()+'/image_p/net_pk.pkl')
            query_list.append(poker_c(pk1))
        if pk2_color[0]==238:
            pk2=image_re.poker_predict(getcwd()+'/pk2_co.png',getcwd()+'/image_p/net_pk.pkl')
            query_list.append(poker_c(pk2))
        if pk3_color[0]==238:
            pk3=image_re.poker_predict(getcwd()+'/pk3_co.png',getcwd()+'/image_p/net_pk.pkl')
            query_list.append(poker_c(pk3))
        if pk4_color[0]==238:
            pk4=image_re.poker_predict(getcwd()+'/pk4_co.png',getcwd()+'/image_p/net_pk.pkl')
            query_list.append(poker_c(pk4))
        if pk5_color[0]==238:
            pk5=image_re.poker_predict(getcwd()+'/pk5_co.png',getcwd()+'/image_p/net_pk.pkl')
            query_list.append(poker_c(pk5))       
        #识别出allmoney,costmoney,getmoney 
        try:
            cost_temp,str_zt=image_re.aboutMoney(getcwd()+'/zt_co.png')
            allmoney,str_temp=image_re.aboutMoney(getcwd()+'/am_co.png')
            getmoney,str_temp=image_re.aboutMoney(getcwd()+'/dz_co.png')
            if cost_temp==999999999:
                costmoney=allmoney
            else:
                costmoney=cost_temp
            #计算出应该的动作
            print allmoney, costmoney, getmoney, query_list,str_zt
            #Myrecord(allmoney, costmoney, getmoney, query_list,str_zt)
            
            str_temp,flag=Myanswer(allmoney, costmoney, getmoney, query_list,str_zt)
            print str_temp
            do_main(flag)
        except Exception,e:
            Myrecord(allmoney, costmoney, getmoney, query_list,str_zt)
            do_main(0)
            print e
    else:
        #清空变量
        print '等待中....'
        continue
    #sleep(1)

            
    
    
