# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def flood_plot(Q, Q_base):
    """
    Objective
    ---------
    绘图
    Parameters
    ----------
    params：参数（list）
    Returns
    -------
    """
    ###常规的绘图，后面多种计算方法对比用循环即可绘制所有结果的图
    x = range(len(Q))
    # 指定画布大小
    plt.figure(dpi=150, figsize=(12, 4))
    plt.plot(x, Q, label=u'real')
    plt.plot(x, Q_base, label=u'simu')
    plt.legend()
    plt.show()




def Eckhardt(streamflow_list, BFI=0.8,alpha=0.925,invert=True):
    #这里就是写滤波方程，Alpha为f1参数
    # Alpha 在 0 ~1，首先判断输入是否合理
    if BFI < 0 or BFI > 1:
        print("BFI must be between 0 and 1.")
    elif alpha < 0 or alpha > 1:
        print("alpha must be between 0 and 1.")

    #参数正确进行下一步
    else:
        baseflow_list = []#构建空List

        baseflow_list.append(streamflow_list[0])#通过左边公式可以看出第一个Qd是未知的将其定义为第一个值，

        for i in range(1,len(streamflow_list)):
            #构建循环计算
            currentStreamflow = streamflow_list[i]#定义Qi,
            
            #这里计算
            baseflow_value = ((1-BFI)*alpha*baseflow_list[i-1] + (1-alpha)*BFI*currentStreamflow)/(1-alpha*BFI)
            # 将左边的公式抄下来，
            # 就是Q，out是Qd,下一步计算的径流不能高于原来的值，取较小的一个
            baseflow_value = min(baseflow_value,currentStreamflow)#min 函数取小值

            baseflow_list.append(baseflow_value)#计算结果append到结果的List
        #invert是代表要不要二次滤波，True 是 False-否，利用递归进行反向滤波
        if invert:
            baseflow_list = Eckhardt(baseflow_list[::-1], BFI, alpha, invert=False)[::-1]
    return baseflow_list


if __name__ == "__main__":
    #写在前面  对于我们的数据处理只需要修改两个地方

    file1 = "./data.xlsx"##将文件放入文件夹，第一个地方，文件名
    df_ce = pd.read_excel(file1, sheet_name='Sheet1')#加载文件，读取文件指定表，第二个地方子表名
    # print(df_ce)
    # 看一下读取的数据,需要第三列数据
    # print(df_ce.iloc[:, 2])
    # 已经取到第三列数据，将数据转为List,首先将数据获取转List

    data = df_ce.iloc[:, 2].values.tolist()#data.iloc[:, 1].values.tolist()我们这里是第三列



    # 这里看一下咱们获取的数据，转好了，接下来我们就去编写这个滤波函数
    blow = Eckhardt(data, 0.8, 0.925, True)#对于invert，默认为二次滤波，设置为False即一次滤波，这里自己设定


    # # 这里我们将分割好基流的数据计算了出来
    flood_plot(data, blow)#下一步是绘制计算结果的图

    blow = pd.DataFrame(blow, columns=['baseflow']) #将blow转为Dataframe这是一列数据 只有一个表头
    dataout = pd.concat([df_ce,blow], axis=1)#这里我们将输入数据跟计算的基流合并列合并 axis=1
    # print(dataout)#看一下数据没问题就导出
    # dataout.to_csv('./dataout_Eckhardt.csv', encoding='utf_8_sig')###encoding='utf_8_sig'预防中文乱码
