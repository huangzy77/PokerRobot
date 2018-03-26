#-*-encoding:utf-8-*-
#图像识别代码
import pytesseract
from PIL import Image 
#import matplotlib.pyplot as plt
import numpy as np
import image_pre
from os import path,walk,getcwd
from sklearn import preprocessing,svm,externals,naive_bayes,neural_network

'''

test2=img2.histogram()

x=np.arange(1024)
test1_np=np.array(test1) 
test2_np=np.array(test2)
plt.plot(x,test1_np)  
plt.plot(x,test2_np) 
plt.show()

'''
'''
#辅助函数————对比两个图像的空间距离
def distance(img1,img2):
    #首先将图像二值化,然后转换成np.array
    img1_array=np.array(img1.convert('1'))
    img2_array=np.array(img2.convert('1'))
    img1.show()
    img2.show()
    #返回欧式距
    return np.linalg.norm(img1_array^img2_array)
'''
#使用sklearn进行学习后判断
#辅助函数--训练（输入训练用图片文件夹地址，保存一个net.pkl到程序文件夹）
def train_p(path_str):#给出文件夹所在的地址，生成训练数据集合和目标集合，进行训练，完成后将结果保存为pkl
    train_data=[]#用来存储训练数据和目标数据
    target_data=[]
    for (root, dirs, files) in walk(path_str):
        for filename in files:
            #获取训练数据
            img_temp=image_pre.poker_co(Image.open(path_str+filename, mode="r"))
            img_array=np.array(img_temp.convert('1'))
            train_data.append(img_array)
            #获取目标数据
            #target_temp1=float(str(ord(filename[7:-4][0]))+filename[7:-4][1:])
            fn_temp=0.0
            if filename[7:-4][0]=='r':
                fn_temp=int('1'+filename[7:-4][1:])
            if filename[7:-4][0]=='b':
                fn_temp=int('2'+filename[7:-4][1:])
            if filename[7:-4][0]=='m':
                fn_temp=int('3'+filename[7:-4][1:])
            if filename[7:-4][0]=='f':
                fn_temp=int('4'+filename[7:-4][1:])  
            target_data.append(fn_temp)
    #将原始数据装换为array,并归一化
    train_data_array=np.array(train_data)
    target_data_array=np.array(target_data)
    #target_data_array=preprocessing.scale(np.array(target_data))   
    #用分类器训练
    nsamples, nx, ny = train_data_array.shape
    d2_train_data_array = train_data_array.reshape((nsamples,nx*ny))
    #net = neural_network.MLPClassifier(solver='lbfgs', alpha=1e-3,hidden_layer_sizes=(2*nx*ny, 1), random_state=1,max_iter=200)
    net= svm.SVC()
    net.fit(d2_train_data_array, target_data_array)
    #保存训练数据
    externals.joblib.dump(net,'net_ps.pkl')
    
#辅助函数--输入一个预测图片地址，返回一个预测结果
def poker_predict(img_path,net_path):#输入image,net的地址
    #处理图片数据
    img_temp=image_pre.poker_co(Image.open(img_path, mode="r"))
    img_array=np.array(img_temp.convert('1'))
    pre_data_array=np.array(img_array)
    nx, ny = pre_data_array.shape
    d2_pre_data_array = pre_data_array.reshape((1,nx*ny))
    #加载同文件夹下的net.pkl,并预测
    net=externals.joblib.load(net_path)   
    result_int=net.predict(d2_pre_data_array)
    return result_int[0]

#辅助函数--金额识别（用于总金额和跟随金额的识别，输入img_path，输出int）
def aboutMoney(img_path):
    global mz_int
    img_temp=Image.open(img_path, mode="r")
    try:
        text = pytesseract.image_to_string(img_temp,config='-l chi_sim')
        text.replace(' ','')
        #这是状态的情况
        if text[0]==u'全':
            #让牌的金额
            money=999999999
            return money,text[0]
        if text[0]==u'让':
            #让牌的金额
            money=mz_int
            return money,text[0]
        if text[0]==u'跟':
            #跟的金额
            if text[-1]==u'万':
                money=int(float(text[1:-1])*10000)
            else:
                money=int(text[1:])
            return money,text[0]
        #底池的情况
        if text[2]==u':':
            if text[-1]==u'万':
                money=int(float(text[3:-1])*10000)
            else:
                money=int(text[3:])
            return money,text[0]
        #allmoney
        else:
            if text[-1]==u'万':
                money=int(float(text[0:-1])*10000)
            else:
                money=int(text)
            return money,text[0]
    except Exception,e:
    #啥都不是了
        money=mz_int
        return money,text[0]

#辅助函数--获取区域块的颜色
def get_colornum(img_path,region):#获取指定像素点的颜色值（输入图片地址和像素点坐标）
    img=Image.open(img_path, mode='r')
    img.convert('RGBA')
    a=img.getpixel(region)
    return a        
    
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
#辅助函数--专门用来获取盲注值
mz_int=0
def get_mz():
    global mz_int
    mz_str=raw_input('盲注多少？')
    mz_int=int(mz_str)
    return mz_int 
#函数测试
#train_p('/home/younghunter/桌面/train/')#训练样本并获net.pkl
#print poker_c(poker_predict('/home/younghunter/桌面/ps2_co.png',getcwd()+'/net_ps.pkl'))
#测试颜色获取
#a=get_colornum('/home/younghunter/桌面/ps1_co_f5.png',(8,88))#这是pk的判断位置（8,118），ps判断位置（8,88），zt判断位置（8,8） 
#print a[0]

#测试汉字识别
#img=Image.open('/home/younghunter/桌面/dz/dz_co_1.32w.png',mode='r')
#text = pytesseract.image_to_string(img,config='-l chi_sim')
#print text
#get_mz()
#print aboutMoney('/home/younghunter/桌面/dz_co.png')