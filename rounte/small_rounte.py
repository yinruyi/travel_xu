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

class Rounte():
    #景点之间走动的次数
    def tran_data(self, mainAttraction, data):
        result = []
        for i in xrange(len(data)):
            temp_result = []
            temp = data[i].split()
            if len(temp) > 0:
                for j in xrange(len(temp)):
                    new_temp = temp[j].split("/")
                    if len(new_temp) == 2:
                        if new_temp[1] == "tttttttt" and new_temp[0] in mainAttraction:
                            temp_result.append(new_temp[0])
            result.append(temp_result)
        return result

    def count(self, dataset):
        resultSet = {}
        for i in xrange(len(dataset)):
            if dataset[i] in resultSet:
                resultSet[dataset[i]] += 1
            else:
                resultSet[dataset[i]] = 1
        return resultSet

    def getRounte(self,mainAttraction):
        data = self.read_txt(abspath+"//data//tongjiblog998.txt")
        #mainAttraction = self.read_txt(abspath+"//data//mainAttraction.txt")
        data = self.tran_data(mainAttraction, data)
        rounteList = []
        for i in xrange(len(data)):
            temp = data[i]
            if len(temp) > 1:
                for j in xrange(len(temp)-1):
                    if temp[j] != temp[j+1]:
                        rounteTemp = (temp[j],temp[j+1])
                        rounteList.append(rounteTemp)
        rounteSet = self.count(rounteList)
        return rounteSet

class hits():
    def getHits(self,mainAttraction):
        resultSet = {}
        hits_data = self.read_txt(abspath+"//data//hits.txt")
        #mainAttraction = self.read_txt(abspath+"//data//mainAttraction.txt")
        hitsSet = self.transData(hits_data)
        for k,v in hitsSet.items():
            if k in mainAttraction:
                resultSet[k] = float(v)
        #print resultSet,len(resultSet)
        resultSet = self.set0_1Result(resultSet)
        return resultSet


    def transData(self, dataset):
        Set = {}
        for i in xrange(len(dataset)):
            temp = dataset[i]
            temp = temp.split(u",")
            Set[temp[0]] = temp[1]
        return Set

    def set0_1Result(self, dataset):
        temp = []
        for k,v in dataset.items():
            temp.append(v)
        max_num = max(temp)
        for k,v in dataset.items():
            dataset[k] = v*1.0/max_num
        return dataset

class sentiment():
    def getSentiment(self,mainAttraction):
        sentimentResult = {}
        #mainAttraction = self.read_txt(abspath+"//data//mainAttraction.txt")
        sentiment_data = self.read_txt(abspath+"//data//sentiment.txt")
        sentimentSet = self.transData(sentiment_data)
        for k,v in sentimentSet.items():
            if k in mainAttraction:
                sentimentResult[k] = float(v)
        sentimentResult = self.set0_1Result(sentimentResult)
        return sentimentResult

class feature():
    def getFeature(self,mainAttraction):
        attraction_featureSet = {}
        #mainAttraction = self.read_txt(abspath+"//data//mainAttraction.txt")
        for i in xrange(len(mainAttraction)):
            path = abspath+"//data//result_data//"+str(i)+".txt"
            txt = self.read_txt(path)
            txtFeature = self.txt2feature(txt)
            #print txtFeature
            if (txtFeature[0] == "" or txtFeature[0] == " ") and len(txtFeature) == 1:
            #if len(txtFeature) == 1:
                attraction_featureSet[mainAttraction[i]] = []
            else:
                attraction_featureSet[mainAttraction[i]] = txtFeature
        attraction_featureSet = self.fixFeatureSetResult(attraction_featureSet)
        attraction_featureSet = self.set0_1Result(attraction_featureSet)
        return attraction_featureSet

    def fixFeatureSetResult(self, dataset):
        result = {}
        for k,v in dataset.items():
            result[k] = len(list(set(v)))
        return result

    def txt2feature(self, dataset):
        feature = []
        for i in xrange(len(dataset)):
            temp = dataset[i].split(",")
            feature.append(temp[0])
        return feature

class DataAnalysis(pretreatment, Rounte, hits, sentiment, feature):
    def makePlus(self, rounteSet,  section, method = "AX"):
        #计算AX之和或者XB之和
        result = []
        if method == "AX":
            for k,v in rounteSet.items():
                if k[0] == section:
                    result.append(v)
        elif method == "XB":
            for k,v in rounteSet.items():
                if k[1] == section:
                    result.append(v)
        #print result
        result = sum(result)
        return result

    def transKind(self, kind):
    	new_kind = []
    	for i in xrange(len(kind)):
    		temp = kind[i].split(",")
    		new_kind.append(temp)
    	return new_kind


    def main(self):
        rounteResult = {}
        kind = self.read_txt(abspath+"//data//kind.txt")
        kind = self.transKind(kind)
        mainAttraction = kind[4]##################修改第几景区
        print "test"
        rounteSet = self.getRounte(mainAttraction)
        #print rounteSet,len(rounteSet)
        rounteSet01 = self.set0_1Result(rounteSet)
        rounteSet = self.getRounte(mainAttraction)#路径次数
        hitsSet = self.getHits(mainAttraction)#hits分数
        #print hitsSet
        sentimentSet = self.getSentiment(mainAttraction)#sentiment分数
        #print sentimentSet
        featureSet = self.getFeature(mainAttraction)
        print featureSet
        for k,v in rounteSet.items():
            AXplus = self.makePlus(rounteSet,k[0],"AX")
            #print AXplus
            XBplus = self.makePlus(rounteSet,k[1],"XB")
            A_part = v*hitsSet[k[0]]*sentimentSet[k[0]]*featureSet[k[0]]/AXplus
            B_part = v*hitsSet[k[1]]*sentimentSet[k[1]]*featureSet[k[1]]/XBplus
            point = rounteSet01[k]*(A_part+B_part)
            rounteResult[k] = point
        print rounteResult#得到结果
        writeResutlt = []
        for k,v in rounteResult.items():
            temp = [k[0],k[1],v]
            writeResutlt.append(temp)
        self.writeMatrix(writeResutlt,"result.txt")

if __name__=='__main__':
    DataAnalysis().main()       