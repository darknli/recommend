# -*- coding: utf-8 -*-
"""
Created on Fri Apr 14 12:16:31 2017

@author: Darkn
"""

import math
import random
class RLTMF():
    def InitList_movielens(self, filenameTest):
        'initialize each of list of data'


        self.train = []
        file = open(filenameTest)
        records = file.readlines()
        records = records[1:]
        self.test = []
        user = set()
        item = set()
        print(len(records))
        
        if '.csv' in filenameTest:
            for record in records:
                fields = record.split(',')
                user.add(fields[0])
                item.add(fields[1])
                if random.randint(1,5)>1:
                    self.train.append(fields[0:3])
                else:
                    self.test.append(fields[0:3])
        elif '.dat' in filenameTest:
            for record in records:
                fields = record.split('::')
                user.add(fields[0])
                item.add(fields[1])
                if random.randint(1, 5)>1:
                    self.train.append(fields[0:3])
                else:
                    self.test.append(fields[0:3])
                    
        print(len(user), len(item))   
#        print('reading the data was done!\nthe length of train is ',len(self.train))
#        print('length of test is ',len(self.test))
        
    
    def __init__(self, N, f=2):
        
        self.F = f
        self.n = N#迭代次数
        self.a = 0.005
        self.b = 0.0
    
    
        
    
    def InitLFM(self):
        'initialize p,q:p is the dictionary of users-factors;q is the dictionary of items-factors'
        self.p = dict()
        self.q = dict()
        for u, i, rui in self.train:
            if u not in self.p:
                self.p[u] = [round(random.uniform(0,1),3) for x in range(self.F)]
            if i not in self.q:
                self.q[i] = [round(random.uniform(0,1),3) for x in range(self.F)]
    
    #    print('Initialization of p and q was done!')

    def fit(self):
        'learn the latent factor model return p,q'
        self.InitLFM()
        for step in range(self.n):
            train_mae = 0.0
            for u, i, rui in self.train:
                pui = self.Predict(u, i)
                eui = float(rui) - float(pui)
                train_mae += abs(eui)
    #            print(rui,'-',pui,'=',eui)
                for f in range(self.F):
                    
                    p1 = self.a * (round(self.q[i][f] * eui, 3) - self.b * self.p[u][f])
                    q1 = self.a * (round(self.p[u][f] * eui, 3) - self.b * self.q[i][f])
                    self.p[u][f] = round(p1 + self.p[u][f], 3)
                    self.q[i][f] = round(q1 + self.q[i][f],3)
    #        if step%10 == 0:
    #            a *= 0.95
            self.a *= 0.9
           # RMSE(test, p, q)
           # rmse = RMSE(test, p, q)
           # mae = MAE(test, p, q)
#            print(step,':%.8f|%.8f'%(0.1, self.MAE('test')))
    #        print("RMSE is", rmse, end = '')
            yield step, train_mae / len(self.train)
    #         yield " %3d epoch :MAE is %f\n" % (step, train_mae/len(self.train))
        yield "finish!"
    
    def Predict(self, u, i):
        'calcuate the predict of user to item'
        Sum = 0
        if len(self.p[u]) == len(self.q[i]):
            for f in range(self.F):
                Sum += self.p[u][f] * self.q[i][f]
            if Sum < 1:
                Sum = 1
            if Sum > 5:
                Sum = 5
    #        print(u,'and', i)
    #        print(p[u])
    #        print(q[i])
    #        print(Sum,'\n')
            return round(Sum, 3)
        else:
            return 0
    
    
    def RecordModel(self):
        path = 'LFM'
        import os
        
        if not os.path.exists(path):
            os.makedirs(path)
        q_file = 'q.txt'
        p_file = 'p.txt'
        test_file = 'test.txt'
        train_file = 'train.txt'
        
        q_path = path + '/' + q_file
        p_path = path + '/' + p_file
        test_path = path + '/' + test_file
        train_path = path + '/' + train_file
        
        file = open(q_path, 'w')
        file.write(str(self.q))
        file.close()
        
        file = open(p_path, 'w')
        file.write(str(self.p))
        file.close()
        
        file = open(test_path, 'w')
        file.write(str(self.test))
        file.close()
        
        file = open(train_path, 'w')
        file.write(str(self.train))
        file.close()
        
        print('Recording the model is successful!')
        
        
    def ReadModel(self, setTrain = False):
        path = 'model'
        q_file = 'q.txt'
        p_file = 'p.txt'
        test_file = 'test.txt'
        train_file = 'train.txt'
        
        
        q_path = path + '/' + q_file
        p_path = path + '/' + p_file
        test_path = path + '/' + test_file
        train_path = path + '/' + train_file


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
        
        if setTrain:
            file = open(train_path, 'r')
            pstr = file.read()
            self.train = eval(pstr)
            file.close()
        
        print('Reading the model is successful!')
    
    
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
    
    def MAE(self, style = 'test'):
        'Score prediction Method of MAE'
        Sum = 0
        if style == 'test':
            for u, i, rui in self.test:
                if u in self.p and i in self.q:
                    Sum += math.fabs(float(rui) - self.Predict(u, i))
            return Sum/len(self.test)
        else:
            for u, i, rui in self.train:
                if u in self.p and i in self.q:
                    Sum += math.fabs(float(rui) - self.Predict(u, i))
            return Sum/len(self.train)
        
    def setEvalPara(self,N = 10):
        '推荐列表长度，通常top10'
        self.N = N
        self.item_test_all = set()
        self.user_test_all = set()
        for u, i, r in self.train:
            self.item_test_all.add(i)
            self.user_test_all.add(u)
        print('物品：', len(self.item_test_all))    
        print('用户：', len(self.user_test_all))
        print('推荐数：', self.N)
        print('评估参数设置完成！')
            
    def TopN(self, user, choice='NOT_RATING'):
        if user not in self.p:
            return None
        user_item = []
        if choice == 'NOT_RATING':
            for i in self.item_test_all:
                if i in self.q:
                    
                    r = self.Predict(user, i)
                    user_item.append((i,r))
                    
            try:        
                return set([elem[0] for elem in (sorted(user_item,key = lambda item:item[1], reverse = True))][:self.N])
            except BaseException:
                print(user_item)
                exit(0)
        else:
            for i in self.item_test_all:
                if i in self.q:
                    r = self.Predict(user, i)
                    user_item.append((i,r))
            return sorted(user_item,key = lambda item:item[1], reverse = True)[:self.N]
        
    def Coverage(self):
        item_len = set()
        item_all = set()
        self.get_userDict()
        
#        for u,i,r in self.train:
#            for user, item, rating in self.test:
#                if u == user:
#                    item_all.add(item)
#            item_list = self.TopN(u, choice = 'WITH_RATING')
#            for item in item_list:
#                item_len.add(item[0])    
#
        for u in self.user_test_all:
            if u not in self.user_dict:
                continue
            if u in self.p:
                item_list = self.TopN(u, choice = 'NOT_RATING')
                item_len = item_len|item_list
                item_all = item_all|self.user_dict[u]
        return '覆盖率 %.3f\n' % (len(item_len)/len(self.item_test_all))

    def PrecisionRecall(self):
        user_list = {}
        for u, i, r in self.train:
            if u not in user_list:
                user_list[u] = set()  
            user_list[u].add(i)
            
        len_recall = 0
        len_precision = 0
        hit = 0
        for u in self.user_test_all:
            if u in self.p:
                rec_list = self.TopN(u)
    #            print([elem[0] for elem in user_list[u]])
    #            rec_set = set(elem[0] for elem in rec_list)
    #            user_set = set([elem[0] for elem in user_list[u]])
    #            if not len(user_set) < self.N:
    #            if len(user_list[u]&rec_list) != 0:
    #                print(u)
                hit += len(user_list[u]&rec_list)
                len_recall += len(user_list[u])
                len_precision += self.N
            
        return '准确率 %.3f\n' % (hit/len_precision) + '召回率%.3f\n' % (hit/len_recall)
        
        
        
    def get_itemDict(self):
        self.item_dict = {}
        file = open('jester_ratings.csv')
        records = file.readlines()
        records = records[1:]
        for record in records:
            fields = record.split(',')
            if fields[1] not in self.item_dict:
                self.item_dict[fields[1]] = set()
            self.item_dict[fields[1]].add(fields[0])
            
    def get_userDict(self):
        self.user_dict = {}
        for u, i, r in self.train:
            if u not in self.user_dict:
                self.user_dict[u] = set()
            self.user_dict[u].add(i)
        self.user = set()
            
            
    def similarity(self, item_1, item_2):
#        print(self.item_dict[item_1] , self.item_dict[item_2])
        length_12 = len(self.item_dict[item_1] & self.item_dict[item_2])
        if length_12 == 0:
            return 0
        else:
            return length_12/math.sqrt(len(self.item_dict[item_1]) * len(self.item_dict[item_2]))
        
    
    def Diversity(self):
        self.get_itemDict()
        sim_dict = {}
        diver_all = 0          #总的多样性
        
        for u in self.user_test_all:
            pop_set = set()
            if u not in self.p:
                continue
            rec_set = self.TopN(u)
            diversity = 0       #每个用户推荐列表的多样性
            for i1 in rec_set:
                pop_set.add(i1)             #将遍历过的元素加入pop_set里
                next_set = rec_set - pop_set
                for i2 in next_set: #将没遍历过的元素的集合进入第二次迭代当中
                    if i1 < i2:
                        tpl = (i1, i2)
                    else:
                        tpl = (i2, i1)
                    if tpl not in sim_dict:
                        sim_dict[tpl] = self.similarity(i1, i2)
                    diversity += sim_dict[tpl]   
            u_list = len(rec_set)
            additem = 1 - diversity * 2 / (u_list * (u_list - 1))
#            print(additem)
            diver_all += additem
        diver_all /= len(self.user_test_all)
        return '多样性:%.3f\n' % diver_all
        
if __name__ == '__main__':

    #for i in range(100):
    #    Ff = F + i * 20
    #    print('F is',Ff)
    #    LearningLFM(train, Ff, n, a, b, test)
    model = RLTMF(10, 10)
    model.InitList_movielens('ratings.dat')
    for epoch_info in model.fit():
        print(epoch_info)
    # # model.fit()
    model.RecordModel()
    # model.ReadModel(setTrain = True)
    # #
    # model.setEvalPara(70)
    # model.Coverage()
    # model.PrecisionRecall()

    # model.Diversity()
    del model


