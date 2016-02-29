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


class Rounte():#景区之间走动的次数
    def trans_data(self, kind, data):
        result = []
        kind = self.transKind(kind)
        #print kind
        #if kind.has_key(u"水立方"):
        #    print "ss"
        #else:
        #    print "ssss"
        for i in xrange(len(data)):
            #print data[i]
            temp_result = []
            temp = data[i].split()
            #print temp
            if len(temp) > 0:
                for j in xrange(len(temp)):
                    new_temp = temp[j].split("/")
                    if len(new_temp) == 2:
                        #print new_temp
                        if  new_temp[1] == "tttttttt" and kind.has_key(new_temp[0]):
                            temp_result.append(kind[new_temp[0]])
            #print temp_result
            result.append(temp_result)

            #break
        return result

    def transKind(self, kind):
        #print len(kind)
        result = {}
        direction = "ABCDEF"
        for i in xrange(len(kind)):
            temp = kind[i].split(",")
            for j in xrange(len(temp)):
                result[temp[j]] = direction[i]
        return result

    def count(self, dataset):
        resultSet = {}
        for i in xrange(len(dataset)):
            if dataset[i] in resultSet:
                resultSet[dataset[i]] += 1
            else:
                resultSet[dataset[i]] = 1
        return resultSet

    def getRounte(self):
        kind = self.read_txt(abspath+"//data//kind.txt")
        data = self.read_txt(abspath+"//data//tongjiblog998.txt")
        data = self.trans_data(kind, data)#得到景区间走动的list
        rounteList = []
        for i in xrange(len(data)):
            #print data[i]
            temp = data[i]
            if len(temp) > 1:
                for j in xrange(len(temp)-1):
                    if temp[j] != temp[j+1]:
                        #rounteTemp = "/".join([temp[j],temp[j+1]])
                        rounteTemp = (temp[j],temp[j+1])
                        rounteList.append(rounteTemp)
        #print rounteList,len(rounteList)
        rounteSet = self.count(rounteList)#景区间走动的次数
        print rounteSet,len(rounteSet)
        return rounteSet

class hits():#景区hits得分
    def getDriectionHits(self):
        hitsResult = {}
        kind = self.read_txt(abspath+"//data//kind.txt")
        hits_data = self.read_txt(abspath+"//data//hits.txt")
        kind = self.transKind(kind)
        hitsSet = self.transData(hits_data)
        #print kind
        #print hitsSet,kind
        direction = "ABCDEF"
        for k,v in kind.items():
            if v in hitsResult:
                hitsResult[v] += float(hitsSet[k])
            else:
                hitsResult[v] = float(hitsSet[k])
        print hitsResult
        hitsResult = self.transHitsResult(hitsResult)
        print hitsResult
        return hitsResult
            
    def transData(self, dataset):
        Set = {}
        for i in xrange(len(dataset)):
            temp = dataset[i]
            temp = temp.split(u",")
            Set[temp[0]] = temp[1]
        return Set

    def transHitsResult(self, dataset):
        temp = []
        for k,v in dataset.items():
            temp.append(v)
        max_num = max(temp)
        for k,v in dataset.items():
            dataset[k] = v/max_num
        return dataset



class DataAnalysis(pretreatment, Rounte, hits):
    pass



if __name__=='__main__':
    DataAnalysis().getDriectionHits()