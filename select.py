#coding:utf-8
import sys
import os

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
        print dataset[1]

        

class DataAnalysis(pretreatment, treatment):
    pass



if __name__=='__main__':
    data = DataAnalysis().read_txt(abspath+'//data//beijing_attraction.txt')#主要景点数据
    data = DataAnalysis().read_txt(abspath+"//data//beijing_all.txt")#景点与景点之间的联系数据
    data = DataAnalysis().findCinnection(data)
    #print data[0]