#coding:utf-8
import sys
import os
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
from numpy import * 
reload(sys)
sys.setdefaultencoding('utf-8')
abspath = os.getcwd()

class pretreatment():
    """预处理"""
    def __init__(self):
        pass
    def read_txt(self,txtPath,coding = 'utf-8'):
        import codecs
        f = codecs.open(txtPath,'r',coding).readlines()
        f[0] = f[0].replace(u"\ufeff",u"")
        dataset = []
        for line in f:
            line = line.replace(u"\r\n",u"")
            line = line.replace(u"\n",u"")
            dataset.append(line)
        return dataset

    def writefile(self, dataset):
        #for i in xrange(len(data#)):
        #    data[i][2] = str(data[i][2])
        #    data[i][3] = str(data[i][3])
        #    print data[i]
        #    #break
        for i in xrange(len(dataset)):
            temp = dataset[i]
            if len(temp) >= 1:
                for j in xrange(len(temp)):
                    temp[j] = str(temp[j])
            dataset[i] = temp
        for i in xrange(len(dataset)):
            dataset[i] = ",".join(dataset[i])
        string = "\n".join(dataset)
        open("result.txt","w").write(string)

    def test():
    	pass

class treatment():
    def __init__(self):
        pass
    def makeTuple(self, dataset, mark = u" "):
        for i in xrange(len(dataset)):
            dataset[i] = dataset[i].split(mark)
        return dataset
    
    def findConnection(self):
        beijing_attraction = self.read_txt(abspath+'//data//beijing_attraction.txt')#北京主要景点
        #print beijing_attraction
        beijing_all_en = self.read_txt(abspath+'//data//beijing_en.txt')
        #景点名称   频数  景点名称    频数  共现频数    MAXC    MINC    景点名称    景点名称    共现频数    MAXC    MINC
        #print beijing_all_en[0].split(u"\t")
        beijing_all_en = self.makeTuple(beijing_all_en,u"\t")
        #print beijing_all_en[0]
        result = []
        for i in beijing_all_en:
            if i[0] in beijing_attraction and i[2] in beijing_attraction:
                if float(i[5]) >= 0.5:#阈值!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                    #print i
                    result.append((i[0],i[2],i[5],i[6],"1"))#(景点1，景点2，maxc,minc，“main”)
        #print result
        
        kind = self.joinResult([(i[0],i[1]) for i in result])#归类
        temp_attraction = set(beijing_attraction)
        for i in kind:
            temp_attraction = temp_attraction - set(i)
        #print temp_attraction
        for i in list(temp_attraction):
            kind.append([i])
        #print kind
        #self.writefile(kind)
        #print len(result)#归类数目
        #---------------景点归类完成------------------
        beijing_attraction_other = []
        for i in beijing_all_en:
            beijing_attraction_other.extend([i[0],i[2]])
        beijing_attraction_other = list(set(beijing_attraction_other) - set(beijing_attraction))
        #print beijing_attraction_other
        #print len(beijing_attraction_other)
        #北京次要景点
        connection = []#次要景点和主要景点之间的联系
        for i in beijing_attraction_other:
            #print i
            connection_candidate = []#第i次要景点候选和主要景点连接
            for j in beijing_all_en:
                temp = [j[0],j[2]]
                if i in temp:
                    temp.remove(i)
                    if temp[0] in beijing_attraction:
                        connection_candidate.append([j[0],j[2],float(j[5]),float(j[6])])
            #print connection_candidate
            if len(connection_candidate) == 0:
                pass
            elif len(connection_candidate) == 1:
                connection.append((connection_candidate[0][0],connection_candidate[0][1],connection_candidate[0][2],connection_candidate[0][3],"0"))
            else:
                #print self.rankConnection(connection_candidate)
                connection.append(self.rankConnection(connection_candidate))
        #print connection
        #print len(connection)
        for i in connection:
            result.append(i)
        result = self.pluskind(result, kind)
        self.writefile(result)
        return result

    def pluskind(self, result, kind):
        #print kind
        #print len(kind)
        attraction = []
        for i in kind:
            attraction.extend(i)
        #print attraction
        temp = {}
        for i in attraction:
            for j in xrange(len(kind)):
                if i in kind[j]:
                    temp[i] = j
                    break
        print temp
        #print result
        for i in xrange(len(result)):
            result[i] = list(result[i])
        print result[0]
        for i in xrange(len(result)):
            temp_a = result[i][0]
            temp_b = result[i][1]
            if result[i][4] == "1":
                if temp[temp_a] == temp[temp_b]:
                    result[i].append(str(temp[temp_a]))
                else:
                    print "error"
            else:
                if temp_a in temp:
                    result[i].append(str(temp[temp_a]))
                else:
                    result[i].append(str(temp[temp_b]))
        return result






        #print len(temp),len(attraction),len(set(attraction))


    def rankConnection(self, dataset):
        if len(dataset) <= 1:
            return "error"
        #print dataset
        #print len(dataset)
        dataset = np.array(dataset)
        #print dataset
        def npRank(dataset, k):
            #print "$$$$"
            #print dataset
            #print "&&&&&"
            dataset = np.array(dataset)
            k = [k for i in xrange(len(dataset[0]))]
            #print type(dataset)
            temp = dataset.T[array(k)]
            temp = np.lexsort(temp)
            dataset = dataset[temp]
            return dataset
        dataset = npRank(dataset, 2)
        #print dataset
        #print "****"
        if dataset[-1][2] != dataset[-2][2]:
            #print (dataset[-1][0],dataset[-1][1])
            return (dataset[-1][0],dataset[-1][1],dataset[-1][2],dataset[-1][3],"0")
        else:
            new_dataset = []
            for i in dataset:
                if i[2] == dataset[-1][2]:
                    new_dataset.append(i)
            #print new_dataset
            new_dataset = npRank(new_dataset, 3)
            return (new_dataset[0][0],new_dataset[0][1],new_dataset[0][2],new_dataset[0][3],"0")#如果maxc一样，找minc小的那个





    def joinResult(self, dataset):
        #为了归类[(1,2),(2,3),(3,4),(5,6)] -> [[1,2,3,4],[5,6]]
        '''
        print "*****"
        print dataset
        #[(1,2),(2,3),(3,4),(5,6)] -> [[1,2,3,4],[5,6]]
        dataset = [list(i) for i in dataset]
        for i in xrange(len(dataset)-1):
            for j in xrange(i+1,len(dataset)):
                #print (i,j)
                if len(set(dataset[i]) & set(dataset[j])) != 0:
                    dataset[i] = list((set(dataset[i]) | set(dataset[j])))
                    dataset[j] = []
        new_dataset = []
        for i in xrange(len((dataset))):
            if dataset[i] != []:
                new_dataset.append(dataset[i])
        return new_dataset
        '''
        dataset = [list(i) for i in dataset]
        def joinSingle(dataset):
            for i in xrange(len(dataset)-1):
                for j in xrange(i+1,len(dataset)):
                    #print (i,j)
                    if len(set(dataset[i]) & set(dataset[j])) != 0:
                        dataset[i] = list((set(dataset[i]) | set(dataset[j])))
                        dataset[j] = []
            return dataset
        dataset = joinSingle(dataset)
        while [] in dataset:
            new_dataset = []
            for i in xrange(len(dataset)):
                if dataset[i] != []:
                    new_dataset.append(dataset[i])
            dataset = joinSingle(new_dataset)
        return dataset





class DataAnalysis(pretreatment, treatment):
    pass

def main():
    #data = DataAnalysis().read_txt(abspath+'//data//beijing_attraction.txt')#主要景点数据
    #print data
    data = DataAnalysis().read_txt(abspath+"//data//beijing_all.txt")#景点与景点之间的联系数据
    #[景点1,景点1次数,景点2,景点2次数,共同出现,mc,minc]
    #英文
    #data = DataAnalysis().findConnection_en()
    #中文
    data = DataAnalysis().findConnection()
    print data
    
    
def test():
    pass


if __name__=='__main__':
    main()
    #test()


