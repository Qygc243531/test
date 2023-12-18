import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

#1. 读取数据集数据，并显示数据前5行，同时输出数据大小，并查看数据的详细信息
lipstick=pd.read_csv('lipstick.csv')
print(lipstick.head())
print(lipstick.shape)
print(lipstick.info())

#2. 统计数据表中的缺失值，并删除掉缺失值（10分）；
print(lipstick.isnull().sum())
lipstick.dropna(inplace=True)
print(lipstick.isnull().sum())

#删除掉没用的列“image_src”；
lipstick=lipstick.drop('image_src',axis=1)
print(lipstick.info())

#将“price”列数据转化为 float 类型；
lipstick['price'] = lipstick['price'].str.replace('¥','')
lipstick['price'] = lipstick['price'].astype('float')
print(lipstick.info())

#将“deal”列数据转化为 int 类型；
lipstick['deal'] = lipstick['deal'].str.replace('人付款','')
lipstick['deal'] = lipstick['deal'].astype('int')
print(lipstick.info())

#增加销售额一列，计算方法为产品单价*购买人数
lipstick['销售额']=lipstick['price']*lipstick['deal']

#增加“省份”一列，根据店铺地点筛选出相应省份
lipstick['省份']=lipstick['location'].str.split(' ').str[0]
print(lipstick['省份'].head())

#筛选出购买人数最多的前 30 店铺，并按照购买人数绘制柱状图，画布大小为 10*6,要求使用groupby分组
lipstick_top30=lipstick.groupby('shop')['deal'].sum().sort_values(ascending=False).head(30)
print(lipstick_top30)

sns.set_theme(style='whitegrid', font='SimHei',font_scale=0.8)
plt.figure(figsize=(10,6))
sns.barplot(x=lipstick_top30.values, y=lipstick_top30.index, palette='Blues_d')
plt.title('购买人数最多的前30店铺')
plt.xlabel('店铺名称')
plt.ylabel('购买人数')
plt.show()

#计算每个地区的平均订单量，计算方法为按地区汇总订单总量/地区店铺数，显示平均订单数最多的三个省份/地区，并按照地区的平均订单量绘制柱状图，画布大小为 10*6，
lipstick_mean=lipstick.groupby('省份')['deal'].sum()/lipstick.groupby('省份')['shop'].count()
lipstick_mean=lipstick_mean.sort_values(ascending=False)
print(lipstick_mean.sort_values(ascending=False).head(3))

sns.set_theme(style='darkgrid', font='SimHei',font_scale=0.8)
plt.figure(figsize=(10,6))
sns.barplot(x=lipstick_mean.values, y=lipstick_mean.index, palette='Blues_d')
plt.title('各省份平均订单量')
plt.xlabel('平均订单量')
plt.ylabel('省份')
plt.show()

#. 计算每个店铺的口红单价，并按照从高到低的顺序排序。同时，以单价数据绘制密度曲线图
lipstick_price=lipstick.groupby('shop')['price'].mean().sort_values(ascending=False)

sns.set_theme(style='darkgrid', font='SimHei',font_scale=0.8)
plt.figure(figsize=(10,6))
sns.kdeplot(data=lipstick_price, shade=True)
plt.title('口红单价密度曲线图')
plt.xlabel('口红单价')
plt.ylabel('密度')
plt.show()