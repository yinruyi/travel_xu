#coding:utf-8
import os
import sys
import string
import codecs
reload(sys)
sys.setdefaultencoding('utf-8')
abspath = os.getcwd()

class pretreatment():
    """预处理"""
    def __init__(self):
        pass
    def read_txt(self, txtPath, coding = 'utf-8'):
        import codecs
        f = codecs.open(txtPath,'r',coding).readlines()
        f[0] = f[0].replace(u"\ufeff",u"")
        dataset = []
        for line in f:
            line = line.replace("\r\n","")
            line = line.replace("\n","")
            dataset.append(line)
        return dataset

    def writeMatrix(self, dataset, Path, coding = "utf-8"):
        for i in xrange(len(dataset)):
            temp = dataset[i]
            temp = [str(temp[j]) for j in xrange(len(temp))]
            temp = ",".join(temp)
            dataset[i] = temp
        string = "\n".join(dataset)
        f = open(Path, "a+")
        line = f.write(string+"\n")
        f.close()


class Methods():
    def trans_data(self, kind, data):
        kind = self.transKind(kind)
        print kind
        #if kind.has_key(u"水立方"):
        #    print "ss"
        #else:
        #    print "ssss"

    def transKind(self, kind):
        #print len(kind)
        result = {}
        direction = "ABCDEF"
        for i in xrange(len(kind)):
            temp = kind[i].split(",")
            for j in xrange(len(temp)):
                result[temp[j]] = direction[i]
        return result


    def getRounte(self, kind, data):
        data = self.trans_data(kind, data)

class DataAnalysis(pretreatment, Methods):
    pass



if __name__=='__main__':
    #print "test"
    kind = DataAnalysis().read_txt(abspath+"//data//kind.txt")
    data = DataAnalysis().read_txt(abspath+"//data//tongjiblog998.txt")
    #print data
    DataAnalysis().getRounte(kind, data)