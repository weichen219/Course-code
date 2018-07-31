import math
import random
import matplotlib.pyplot as plt
import numpy as np
from numpy import random


class SimAnneal(object):
    def __init__(self, matrix, T=-1, alpha=-1, stopping_T=-1, stopping_iter=-1):
        self.matrix = matrix
        self.N = len(matrix[0])
        self.T = math.sqrt(self.N) if T == -1 else T
        self.alpha = 0.995 if alpha == -1 else alpha
        self.stopping_temperature = 0.00000001 if stopping_T == -1 else stopping_T
        self.stopping_iter = 100000 if stopping_iter == -1 else stopping_iter
        self.iteration = 1
        self.cur_solution = self.initial_solution()
        self.best_solution = list(self.cur_solution)
        self.cur_fitness = self.fitness(self.cur_solution)
        self.initial_fitness = self.cur_fitness
        self.best_fitness = self.cur_fitness
        self.fitness_list = [self.cur_fitness]
    
    def initial_solution(self):
        initial_job=()
        for i in  list(self.matrix[0]):  
            initial_job = np.append(initial_job,i)
        initial_job=np.random.permutation(initial_job)     
        n=len(self.matrix[0])
        each_pt=()
        process_time=0
        for i in range(0,n):
            j_p = int(np.argwhere(self.matrix[0]==initial_job[i]))
            temp_process_time=self.matrix[1][j_p]
            process_time+=temp_process_time
            each_pt=np.append(each_pt,process_time)
        initial_mft=(sum(each_pt))/n
        print('Initial solution',initial_mft)
        return initial_job

    def fitness(self, sol):
        """ Objective value of a solution """     
        n=len(self.matrix[0])
        each_pt=()
        process_time=0
        for i in range(0,n):
            j_p = int(np.argwhere(self.matrix[0]==sol[i]))
            temp_process_time=self.matrix[1][j_p]
            process_time+=temp_process_time
            each_pt=np.append(each_pt,process_time)
        mean_flow_time=(sum(each_pt))/n
        return mean_flow_time
        

    def p_accept(self, candidate_fitness):
        """
        Probability of accepting if the candidate is worse than current
        Depends on the current temperature and difference between candidate and current
        """
        return math.exp(-abs(candidate_fitness - self.cur_fitness) / self.T)

    def accept(self, candidate):
        """
        Accept with probability 1 if candidate is better than current
        Accept with probabilty p_accept(..) if candidate is worse
        """
        candidate_fitness = self.fitness(candidate)
        if candidate_fitness < self.cur_fitness:
            self.cur_fitness = candidate_fitness
            self.cur_solution = candidate
            if candidate_fitness < self.best_fitness:
                self.best_fitness = candidate_fitness
                self.best_solution = candidate

        else:
            if random.random() < self.p_accept(candidate_fitness):
                self.cur_fitness = candidate_fitness
                self.cur_solution = candidate

    def anneal(self):
        """
        Execute simulated annealing algorithm
        """
        while self.T >= self.stopping_temperature : 
            self.iteration = 0
            while self.iteration < self.stopping_iter:
                candidate = list(self.cur_solution)
                #l = random.randint(2, self.N - 1)
                #i = random.randint(0, self.N - l)
                k = 1 #產生五個候選解進行選擇，將p開根號八次
                p = self.T
                while k <= 3:
                    p = math.sqrt(p)
                    k += 1
                p = p-1 #讓p小於1
                a_probability = random.uniform(0,1) #產生a、b兩個機率，來選擇產生候選解的方法
                b_probability = random.uniform(0,p)
                can1=() #宣告5個空的候選解
                can2=()
                can3=()
                can4=()
                can5=()
                if a_probability >= b_probability:
                    for k in range(1,6): #將2-op產生的放進5個候選解
                        if k==1:
                            l = random.randint(2, self.N - 1)
                            i = random.randint(0, self.N - 1)
                            candidate[i:(i + l)] = reversed(candidate[i:(i + l)])
                            can1=candidate.copy()
                        elif k==2:
                            l = random.randint(2, self.N - 1)
                            i = random.randint(0, self.N - 1)
                            candidate[i:(i + l)] = reversed(candidate[i:(i + l)])
                            can2=candidate.copy()        
                        elif k==3:
                            l = random.randint(2, self.N - 1)
                            i = random.randint(0, self.N - 1)
                            candidate[i:(i + l)] = reversed(candidate[i:(i + l)])
                            can3=candidate.copy()      
                        elif k==4:
                            l = random.randint(2, self.N - 1)
                            i = random.randint(0, self.N - 1)
                            candidate[i:(i + l)] = reversed(candidate[i:(i + l)])
                            can4=candidate.copy()
                        elif k==5:
                            l = random.randint(2, self.N - 1)
                            i = random.randint(0, self.N - 1)
                            candidate[i:(i + l)] = reversed(candidate[i:(i + l)])
                            can5=candidate.copy()
                    can1_sol=self.fitness(can1) #計算5個候選姐的fitness
                    can2_sol=self.fitness(can2)
                    can3_sol=self.fitness(can3)
                    can4_sol=self.fitness(can4)
                    can5_sol=self.fitness(can5)
                    mat = np.array([can1_sol,can2_sol,can3_sol,can4_sol,can5_sol])
                    min_can=np.argmin(mat)
                    if min_can==0:
                        candidate=can1
                    elif min_can==1:
                        candidate=can2
                    elif min_can==2:
                        candidate=can3
                    elif min_can==3:
                        candidate=can4
                    elif min_can==4:
                        candidate=can5 
                else: #隨機產生後選解
                    candidate=np.random.permutation(candidate)
                self.accept(candidate) #計算波茲曼函數
                self.iteration += 1 #同溫層下迭代次數加1
            self.T *= self.alpha #降溫
            #self.iteration = 0
            self.fitness_list.append(self.cur_fitness)

        print('Best fitness obtained: ', self.best_fitness) 
        #print('Job processing sequence',self.best_solution)  
        print('Improvement over initial solution: ',
              (round((self.initial_fitness - self.best_fitness) / (self.initial_fitness), 4))*100,'%')


    def plot_learning(self):
        """
        Plot the fitness through iterations
        """
        plt.plot([i for i in range(len(self.fitness_list))], self.fitness_list)
        plt.ylabel('Fitness')
        plt.xlabel('Annealing Iteration')
        plt.show()
    
    def spt(self):
        """
        SPT
        """
        ptime= self.matrix[1][:]
        spt = np.sort(ptime)
        temp_time=0
        f_time=()
        job_seq =()
        for i in range(0,self.N):
            j_p = int(np.argwhere(ptime==spt[i]))
            temp_time+=spt[i]
            f_time=np.append(f_time,temp_time)
            pit = self.matrix[0][j_p]
            job_seq = np.append(job_seq,pit)
        mean_ftime=sum(f_time)/self.N
        #print('SPT工作加工順序',job_seq)
        #print('SPT平均流程時間',mean_ftime)
        return mean_ftime
