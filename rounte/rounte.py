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
        #print rounteSet,len(rounteSet)
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
        #direction = "ABCDEF"
        for k,v in kind.items():
            if v in hitsResult:
                hitsResult[v] += float(hitsSet[k])
            else:
                hitsResult[v] = float(hitsSet[k])
        #print hitsResult
        hitsResult = self.set0_1Result(hitsResult)
        #print hitsResult
        return hitsResult
            
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
    def getSentiment(self):
        sentimentResult = {}
        kind = self.read_txt(abspath+"//data//kind.txt")
        sentiment_data = self.read_txt(abspath+"//data//sentiment.txt")
        kind = self.transKind(kind)
        sentimentSet = self.transData(sentiment_data)
        #print kind
        #print hitsSet,kind
        #direction = "ABCDEF"
        for k,v in kind.items():
            if v in sentimentResult:
                sentimentResult[v] += float(sentimentSet[k])/5
            else:
                sentimentResult[v] = float(sentimentSet[k])/5
        #print sentimentResult
        sentimentResult = self.set0_1Result(sentimentResult)
        #print sentimentResult
        return sentimentResult

class feature():
    def getFeature(self):
        featureSet = {}
        attraction_featureSet = {}
        mainAttraction = self.read_txt(abspath+"//data//mainAttraction.txt")
        #print mainAttraction
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
        #print attraction_featureSet
        #得到了每个景点锁对应的特征
        kind = self.read_txt(abspath+"//data//kind.txt")
        kind = self.transKind(kind)
        for k,v in kind.items():
            if v in featureSet:
                featureSet[v].extend(attraction_featureSet[k])
            else:
                featureSet[v] = attraction_featureSet[k]
        #print featureSet
        featureSet = self.fixFeatureSetResult(featureSet)
        #print featureSet
        featureSet = self.set0_1Result(featureSet)
        #print featureSet
        return featureSet

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


    def main(self):
        rounteResult = {}
        rounteSet = self.getRounte()
        #print rounteSet
        rounteSet01 = self.set0_1Result(rounteSet)#归一化的路径
        rounteSet = self.getRounte()#路径次数
        #print rounteSet,rounteSet01
        hitsSet = self.getDriectionHits()#hits分数
        #print hitsSet
        sentimentSet = self.getSentiment()#sentiment分数
        #print sentimentSet
        featureSet = self.getFeature()
        #print featureSet
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