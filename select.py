#coding:utf-8
import sys
import os
import networkx as nx
import matplotlib.pyplot as plt
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

    def test():
    	pass

class treatment():
    def __init__(self):
        pass
    def makeTuple(self, dataset):
        for i in xrange(len(dataset)):
            dataset[i] = dataset[i].split()
        return dataset
    
    def findCinnection(self, dataset):
        dataset = self.makeTuple(dataset)
        main_attraction = self.read_txt(abspath+'//data//beijing_attraction.txt')
        #print main_attraction
        #print dataset[1]
        result = []
        for i in dataset:
            if i[0] in main_attraction and i[2] in main_attraction:
                if float(i[5]) >= 0.8:
                    result.append((i[0],i[2]))
        return result

    def drawGraph(self, dataset, weight = 0):
        #weight=1表示画有权重的图，weight=0表示画没有权重的图
        #dataset = [("1","2"),("1","3"),("1","4"),("1","5"),("4","5"),("4","6"),("5","6")]
        #dataset = [("1","2",1),("1","3",4),("1","4",5),("1","5",8),("4","5",7),("4","6",10),("5","6",8)]
        G = nx.Graph()
        if weight == 0:
            G.add_edges_from(dataset)
        else:
            dataset = [(i[0],i[1],1.0*i[2]*0.01) for i in dataset]
            G.add_weighted_edges_from(dataset)
        pos = nx.spring_layout(G)
        nx.draw_networkx_nodes(G,pos)
        nx.draw_networkx_edges(G,pos)
        plt.axis('off')
        plt.savefig("color_nodes.png")
        plt.show()


        

class DataAnalysis(pretreatment, treatment):
    pass



if __name__=='__main__':
    #data = DataAnalysis().read_txt(abspath+'//data//beijing_attraction.txt')#主要景点数据
    #print data
    data = DataAnalysis().read_txt(abspath+"//data//beijing_all.txt")#景点与景点之间的联系数据
    #[景点1,景点1次数,景点2,景点2次数,共同出现,mc,minc]
    data = DataAnalysis().findCinnection(data)
    print data
    #print data[0]
    #dataset = [("1","2",1),("1","3",4),("1","4",5),("1","5",8),("4","5",7),("4","6",10),("5","6",8)]
    DataAnalysis().drawGraph(data)
