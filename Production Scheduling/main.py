from anneal import SimAnneal
import matplotlib.pyplot as plt
import numpy as np
from numpy import random
import random

n=100
upper=150

job_number = np.arange(1,n+1) #建立n個工作

#ptime設為整數
ptime = np.random.choice(upper, n, replace=False) #隨機產生工作的加工時間
test=np.count_nonzero(ptime == 0)
while test==1:
    ptime = np.random.choice(upper, n, replace=False)
    test=np.count_nonzero(ptime == 0)
'''
#ptime設為小數
ptime=([[]])
k=1
while k <= n:
    rand_pt=round(random.uniform(1, 100),4)
    ptime=np.append(ptime,rand_pt)
    k+=1
'''


fitness_list=()
matrix = np.vstack((job_number,ptime)) #將兩個矩陣合併

i=1
while i<=5:
    if __name__ == '__main__':
        sa = SimAnneal(matrix,alpha=0.95,T=100,stopping_iter=100,stopping_T=0.0001) # 
        sa.anneal()
        sa.spt()
        sa.plot_learning()
        each_gap_fitness = round((sa.best_fitness - sa.spt())/sa.best_fitness,8)
        print('Each Time Gap',each_gap_fitness*100,'%')
        print('')
        fitness_list = np.append(fitness_list,sa.best_fitness) 
    i+=1
# print(fitness_list)
print(sa.T)
print(sa.iteration)
mean_fitness = sum(fitness_list)/(i-1)
print('演算法平均值',round(mean_fitness,2))
max_fitness = max(fitness_list)
print('演算法最大值',max_fitness)
min_fitness = min(fitness_list)
print('演算法最小值',min_fitness)
print('SPT最佳解',sa.spt())
gap_fitness = round((mean_fitness - sa.spt())/mean_fitness,4)
print('Gap',gap_fitness*100,'%')
