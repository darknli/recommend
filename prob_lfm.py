# -*- coding: utf-8 -*-
"""
Created on Tue Apr  3 10:14:50 2018

@author: Darkn
"""
import numpy as np
import random
import math
import numpy as np
import matplotlib.pyplot as plt
from scipy import special


class BLFM:
    def InitList_movielens(self, filename):
        'initialize each of list of data'


        self.train = []
        self.test = []
        with open(filename) as f:
            token = ','
            if '.dat' in filename:
                token = '::'
            lines = f.readlines()[1:]
            for line in lines:
                fields = line.strip().split(token)
                self.train.append(fields[:3])
                # if random.randint(1,100) > 1:
                #     self.train.append(fields[:3])
                # else:
                #     self.test.append(fields[:3])
        print('reading the data was done!\nthe length of train is ',len(self.train))
        print('length of test is ', len(self.test))
    
    def __init__(self, filename, N=15):
        self.InitList_movielens(filename)
        self.F = 10
        self.n = N#迭代次数
        self.a = 0.01
        self.b1 = 2.2
        self.b2 = 0.7
        self.init()
        
    def init(self):
        'initialize p,q:p is the dictionary of users-factors;q is the dictionary of items-factors'
        self.y = {}
        self.e1 = {}
        self.e2 = {}
        self.U = set()
        self.I = set()
        self.λ_ = {}
        self.λ = {}
        for u, i, rui in self.train:
            if u not in self.y:
                self.y[u] = [round(random.uniform(6, 10),3) for k in range(self.F)]
                
            if i not in self.e1 :
                self.e1[i] = [round(random.uniform(6,10),3) for k in range(self.F)]
                self.e2[i] = [round(random.uniform(0.1,2),3) for k in range(self.F)]
                
            self.λ_.setdefault(u, {}) 
            self.λ_[u].setdefault(i, [0 for k in range(self.F)])
            self.λ.setdefault(u, {})
            self.λ[u].setdefault(i, [0 for k in range(self.F)])
            self.U.add(u)
            self.I.add(i)
            
        print('initialization has already been completed')
        
    def DelLFM(self):
        del self.a
        del self.b1
        del self.b2
        del self.e1
        del self.e2
        del self.I
        del self.U
        del self.y
        del self.λ
        del self.λ_
        print('released the memories')
        
    def initToVar(self):
        '''初始化y的所有值为var'''
        for key in self.y:
            for k in range(self.F):
                self.y[key][k] = self.a
        
        for key in self.e1:
            for k in range(self.F):
                self.e1[key][k] = self.b1
                         
        for key in self.e2:
            for k in range(self.F):
                self.e2[key][k] = self.b2
    
    
    def RecordModel(self):
        path = 'BPL2222222'
        import os
        
        if not os.path.exists(path):
            os.makedirs(path)
        q_file = 'q.txt'
        p_file = 'p.txt'
        test_file = 'test.txt'
        q_path = path + '/' + q_file
        p_path = path + '/' + p_file
        test_path = path + '/' + test_file
        print(q_path)
        
        
        file = open(q_path, 'w')
        file.write(str(self.q))
        file.close()
        
        file = open(p_path, 'w')
        file.write(str(self.p))
        file.close()
        
        file = open(test_path, 'w')
        file.write(str(self.test))
        file.close()
        
        print('Recording the model is successful!')
        
        
    def ReadModel(self):
        path = 'BPL2222222'
        q_file = 'q.txt'
        p_file = 'p.txt'
        test_file = 'test.txt'
        
        q_path = path + '/' + q_file
        p_path = path + '/' + p_file
        test_path = path + '/' + test_file
        
        
        
        file = open(q_path, 'r')
        qstr = file.read()
        self.q = eval(qstr)
        file.close()
        
        file = open(p_path, 'r')
        pstr = file.read()
        self.p = eval(pstr)
        file.close()
        
        file = open(test_path, 'r')
        pstr = file.read()
        self.test = eval(pstr)
        file.close()
        
        print('Reading the model is successful!')
        
        
        
    
    def InitLFM(self):
        'initialize p,q:p is the dictionary of users-factors;q is the dictionary of items-factors'
        self.p = dict()
        self.q = dict()
        for u, i, rui in self.train:
            if u not in self.p:
                self.p[u] = [round(random.uniform(0,1),3) for x in range(self.F)]
            if i not in self.q :
                self.q[i] = [round(random.uniform(0,1),3) for x in range(self.F)]
    
    #    print('Initialization of p and q was done!')

    def fit(self):
        'learn the latent factor model return p,q'
        No = 1
        for step in range(self.n):
            
            for u, i, r in self.train:
                λ_sum = 0
                rating = float(r)

                y_sum = sum(self.y[u])
                for k in range(self.F):
    #                print('Y:', y[u][k] / y_sum)
    #                print('e1:',e1[i][k]**rating)
    #                print('e2:', e2[i][k]**(5 - rating))
                    self.λ_[u][i][k] = self.y[u][k]* (self.e1[i][k]**rating) *(self.e2[i][k]**(5 - rating))\
                      /(self.e1[i][k] + self.e2[i][k])**5
    #                print(λ_[u][i][k])
    #                λ_[u][i][k] = math.exp(exponent)
                    
                    λ_sum += self.λ_[u][i][k]
                for k in range(self.F):
                    self.λ[u][i][k] = self.λ_[u][i][k]/λ_sum
                    
    #        if No % 80 == 1:
    #            length = 0
    #            for i in λ[u]:
    #                if length > 3:
    #                    break
    #                else:
    #                    length += 1
    #                for k in range(F):
    #                    print('λ[%s][%s][%d]='%(u,i,k),end= '')
    #                    print(λ[u][i][k],'=',end = '')
    #                    print(y[u][k],'*pow(',e1[i][k],',',rating,')*pow(',e2[i][k],',',5 - rating,')',end='')
    #                    print('÷',round(y_sum,3),'÷pow(',round(e1[i][k] + e2[i][k],3),',5)')
    #            print('\n')    
                
    #        初始化y,e1,e2，给定初值  
            self.initToVar()
            for u, i, r in self.train:
                
                rating = float(r)
                
                for k in range(self.F):
                    self.y[u][k] += self.λ[u][i][k]
                    
                    self.e1[i][k] += self.λ[u][i][k] * rating * 1.1
                    self.e2[i][k] += self.λ[u][i][k] * (5 - rating)
            self.p = {}
            self.q = {}
            
            for u in self.U:
                y_sum = sum(self.y[u])
                self.p[u] = [0 for i in range(self.F)]
                for k in range(self.F):
                    self.p[u][k] = self.y[u][k]/y_sum
            
            for i in self.I:
                self.q[i] = [0 for i in range(self.F)]
                for k in range(self.F):
                    self.q[i][k] = self.e1[i][k]/(self.e1[i][k] + self.e2[i][k])
    #        print('y', y[u])
    #        print(e1[i])
    #        print(e2[i])
    #        print('p', p[u])
    #        print('q', q[i])        
#            print(No, ':%.8f|%.8f'%(self.MAE('test'), self.MAE('train')))
            yield (step, self.MAE('train'))
    #        print('%.6f'%MAEAll(p, q))
        yield 'finish!!!'
        self.DelLFM()
    
    def Predict(self, u, i):
        'calcuate the predict of user to item'
        Sum = 0
#        print(self.p[u] ,self.q[i])
        for f in range(self.F):
                Sum += self.p[u][f] * self.q[i][f]
        return Sum * 5
    
    def RMSE(self):
        'Score prediction Method of RMSE'
        Sum = 0
        Variance = 0
        for u, i,rui in self.test:
            if u in self.p and i in self.q:
                pr = self.Predict(u, i)
                Variance = float(rui) - float(pr)
    #            if Variance > 5 or Variance < -5:
    #                print('rui=',rui,' pr=',pr)
    #                print('Variance =',Variance)
                Sum += Variance * Variance
    #    print(Sum)
    #    print(len(test))
        return math.sqrt(Sum/len(self.Test))
    
    def MAE(self, style='test'):
        'Score prediction Method of MAE'
        Sum = 0
        count = 0
        if style == 'test':
            for u, i, rui in self.test:
                if u in self.p and i in self.q:
                    Sum += math.fabs(float(rui) - self.Predict(u, i))
                    count += 1
#                    print((rui) ,':',self.Predict(u, i))
            return Sum/count
        else:
            for u, i, rui in self.train:
                if u in self.p and i in self.q:
                    Sum += math.fabs(float(rui) - self.Predict(u, i))
                    count += 1
                    # print(math.fabs(float(rui) - self.Predict(u, i)))
            return Sum/count
        
    def setEvalPara(self,N = 10):
        '推荐列表长度，通常top10'
        self.N = N+1
        self.item_test_all = set()
        self.user_test_all = set()
        for u, i, r in self.test:
            self.item_test_all.add(i)
            self.user_test_all.add(u)
        print('评估参数设置完成！')
        
        
    def setN(self,N):
        self.N = N+1


    def TopN(self, user, choice = 'WITH_RATING'):
        
        user_item = []
        if choice == 'WITH_RATING':
            for i in self.item_test_all:
                if i in self.q:
                    
                    r = self.Predict(user, i)
                    user_item.append((i,r))
            return set([elem[0] for elem in (sorted(user_item, key=lambda item:item[1])[:self.N])])
        else:
            for i in self.item_test_all:
                if i in self.q:
                    
                    r = self.Predict(user, i)
                    user_item.append((i,r))
            return sorted(user_item,key = lambda item:item[1])[:self.N]
    
    
    def setTestUI(self):
        '在测试集上得到用户和物品的集合'
        self.item_test_all = set()
        self.user_test_all = set()
        for u, i, r in self.test:
            self.item_test_all.add(i)
            self.user_test_all.add(u)
            
        
    def Coverage(self):
        item_len = set()
        for u in self.user_test_all:
             item_list = self.TopN(u)
             for item in item_list:
                 item_len.add(item[0])
        print('覆盖率', len(item_len)/len(self.item_test_all))

    def Precision(self):
        user_list = {}
        for u, i, r in self.test:
            if u not in user_list:
                user_list[u] = []
                user_list[u].append((i, r))
            else:
                for index, item in  enumerate(user_list[u]):
                    if item[1] < r:
                        user_list[u].insert(index, (i, r))
                        if(len(user_list[u]) > self.N-1):
                            user_list[u].pop(len(user_list[u])-1)
                        break       
        for u in self.user_test_all:
            hit = 0
            n_precision = 0
            rec_list = self.TopN(u)
#            print([elem[0] for elem in user_list[u]])
            rec_set = set(elem[0] for elem in rec_list)
            user_set = set([elem[0] for elem in user_list[u]])
#            if not len(user_set) < self.N:
                
            hit += len(user_set&rec_set)
            n_precision += self.N
        print('hit:', hit)
        print('准确率', hit/n_precision)

        
    def getItem_dict(self):
        self.item_dict = {}
        for u, i, r in self.test:
            if i not in self.item_dict:
                self.item_dict[i] = set()
            self.item_dict[i].add(u)
            
        
    def similarity(self, item_1, item_2):
        length_12 = len(self.item_dict[item_1] & self.item_dict[item_2])
        if length_12 == 0:
            return 0
        else:
            return length_12/math.sqrt(len(self.item_dict[item_1]) * len(self.item_dict[item_2]))
        
    
    def Diversity(self):
        self.getItem_dict()
        rec_set = set()
        pop_set = set()
        sim_dict = {}
        diver_all = 0          #总的多样性
        
        for u in self.user_test_all:
            rec_set = self.TopN(u)
            diversity = 0       #每个用户推荐列表的多样性
            for i1 in rec_set:
                pop_set.add(i1)             #将遍历过的元素加入pop_set里
                for i2 in rec_set - pop_set: #将没遍历过的元素的集合进入第二次迭代当中
                    if i1 < i2:
                        tpl = (i1, i2)
                    else:
                        tpl = (i2, i1)
                    if tpl not in sim_dict:
                        sim_dict[tpl] = self.similarity(i1, i2)
                    diversity += sim_dict[tpl]
            u_list = len(rec_set)
            diver_all += 1 - diversity * 2 / u_list * (u_list - 1)
        diver_all /= len(self.user_test_all)
        print('多样性:', diver_all)
