# -*- coding: utf-8 -*-
from PIL import Image
from os import popen,mkdir
from time import sleep
from posix import mkdir

#辅助函数--切割规定区域并保存
def cut_img(im,path_str,w,h):#用于切割整体图片(图像对象，存储路径，图像分辨率)
    #需要获取：开出的5张牌pk，手里的两张牌ps,手里总共还有的钱am,能够收获的钱dz,当前的状态zt.
    print('Original image size: %sx%s' % (w, h))
    #设置一个百分比来截图，以适应不同分辨率的手机
    pk_xy=(0.069,0.166)#开出的一张扑克牌大小所占百分比(95*128)
    ps_xy=(0.058,0.145)#手牌大小（80×108）
    am_xy=(0.092,0.040)#allmoney,手里一共多少钱区域（118×30）
    dz_xy=(0.17,0.04)#底注里有多少钱
    zt_xy=(0.1719,0.0778)#状态，有跟多少，让
    #扑克牌开出来，第一张，左上角位置百分比，后面以此类推poker1_point
    pk1_p=(0.3081,0.373)
    pk2_p=(0.3875,0.373)
    pk3_p=(0.4656,0.373)
    pk4_p=(0.5443,0.373)
    pk5_p=(0.6234,0.373)
    ps1_p=(0.5508,0.6555)#手牌位置
    ps2_p=(0.6138,0.6555)
    am_p=(0.455,0.813)#取allmoney位置
    dz_p=(0.422,0.268)#取底注的位置
    zt_p=(0.6211,0.8972)
    #进行截图,并保存到指定文件夹
    #开出的牌
    pk1_co=im.crop(p_region(pk1_p, pk_xy,w,h))
    pk1_co.save(path_str+'/pk1_co.png')
    pk2_co=im.crop(p_region(pk2_p, pk_xy,w,h))
    pk2_co.save(path_str+'/pk2_co.png')
    pk3_co=im.crop(p_region(pk3_p, pk_xy,w,h))
    pk3_co.save(path_str+'/pk3_co.png')
    pk4_co=im.crop(p_region(pk4_p, pk_xy,w,h))
    pk4_co.save(path_str+'/pk4_co.png')
    pk5_co=im.crop(p_region(pk5_p, pk_xy,w,h))
    pk5_co.save(path_str+'/pk5_co.png')
    #手牌
    ps1_co=im.crop(p_region(ps1_p, ps_xy,w,h))
    ps1_co.save(path_str+'/ps1_co.png')
    ps2_co=im.crop(p_region(ps2_p, ps_xy,w,h))
    ps2_co.save(path_str+'/ps2_co.png')
    #allmoney
    am_co=im.crop(p_region(am_p, am_xy,w,h))
    am_co.save(path_str+'/am_co.png')
    #底注
    dz_co=im.crop(p_region(dz_p, dz_xy,w,h))
    dz_co.save(path_str+'/dz_co.png')
    #状态
    zt_co=im.crop(p_region(zt_p, zt_xy,w,h))
    zt_co.save(path_str+'/zt_co.png')
#辅助函数--通过左上角落的点，计算出区域位置
def p_region(p,xy,w,h):#输入左上角点和大小百分比，和分辨率。输出区域元组（左、顶、右、底）
    left=int(w*p[0])
    top=int(h*p[1])
    right=int(left+w*xy[0])
    bo=int(top+h*xy[1])
    return (left,top,right,bo)
#辅助函数———在判断扑克牌值前进行统一切割，一来减小运算，而来统一大小(小一点不影响识别，30*60)
def poker_co(img):
    return img.crop((0,0,73,103))
    #return img.crop((0,0,50,70))
    #return img.thumbnail(30,60)

'''

#主循环，每隔10秒，采样一次,共采集100次，切割（存入不同文件夹，用于后续训练）
#采集辅助函数    
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
        sleep(0.3)
        popen('adb shell input tap 1150 680')
        sleep(0.5)
        return 0
    else:
        popen('adb shell input tap 620 680')
        sleep(0.5)
        return 0
#辅助函数--获取区域块的颜色
def get_colornum(img_path,region):#获取指定像素点的颜色值（输入图片地址和像素点坐标）
    img=Image.open(img_path, mode='r')
    img.convert('RGBA')
    a=img.getpixel(region)
    return a 

path_str='/home/younghunter/'

print '连接手机，并打开adb模式'
counter_flag=0
while(counter_flag<10000):
    counter_flag=counter_flag+1
    popen('adb shell screencap -p /sdcard/phone_temp.png')#截图
    popen('adb pull /sdcard/phone_temp.png '+path_str)#推送到计算机
    im=Image.open(path_str+'phone_temp.png')#计算机图片加载图片到内存
    w,h=im.size#获取分辨率
    
    mkdir(path_str+str(counter_flag))
    path_temp=path_str+str(counter_flag)+'/'
    cut_img(im,path_temp,w,h)#切割并存储图像
    zt=get_colornum(path_temp+'zt_co.png',(8,8))
    print zt[0] 
    if zt[0]>85 and zt[0]<93:
        do_main(0)
    print '完成第%d次获取、切割和存储'%(counter_flag)

'''

    
    