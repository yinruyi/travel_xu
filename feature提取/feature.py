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
    def makeMatrix(self, dataset):
    	for i in xrange(len(dataset)):
    		pass

class Methods():
    def getAttraction(self, dataset):
        #attractionList = []
        dataset = self.word_tag_fliter(dataset)
        attraction = []
        for i in xrange(len(dataset)):
            attraction_temp = []
            temp = dataset[i]
            temp = temp.split()
            #print temp
            if len(temp) > 0:
                #print "hh"
                for j in xrange(len(temp)):
                    item = temp[j]
                    item = item.split(u"/")
                    if len(item) == 2:
                        attraction_temp.append(item[0])
                        #print attraction_temp
            attraction_temp = list(set(attraction_temp))
            #attractionList.append(attraction_temp)
            attraction.extend(attraction_temp)
        attractionSet = self.count(attraction)#景点名对应出现次数的set
        return attractionSet

    def getFeature(self, featureData, attractionSet):
        resultList = []
        featureSet = self.getAttraction(featureData)
        #print featureSet
        for k,v in featureSet.items():
            temp = []
            mc = v*1.0/min(len(featureData),attractionSet[k])
            if mc >= 0.8 and v >= 5 and attractionSet[k] <= len(featureData):
                temp = [k,v,mc,len(featureData),attractionSet[k]]
                resultList.append(temp)
        return resultList


class treatment():
    def count(self, dataset):
        resultSet = {}
        for i in xrange(len(dataset)):
            if dataset[i] in resultSet:
                resultSet[dataset[i]] += 1
            else:
                resultSet[dataset[i]] = 1
        return resultSet
    def word_tag_fliter(self, data):
        #留下tag里面有的词性
        tag = self.read_txt(abspath+'//data//cixing.txt')
        #print(new_tag)
        for i in xrange(len(data)):
            temp = data[i].split()
            if len(temp) == 0:
                pass
            else:
                for j in range(len(temp)):
                    h = temp[j].split('/')
                    if len(h) == 2:
                        if h[1] not in tag:
                            temp[j] = ' '
            data[i] = ' '.join(temp)
        return data


class DataAnalysis(pretreatment, Methods, treatment):
    pass

if __name__=='__main__':
    data = DataAnalysis().read_txt(abspath+"//data//data.txt")
    mainAttraction = DataAnalysis().read_txt(abspath+"//data//mainAttraction.txt")
    #print mainAttraction[0]+".txt"
    attractionFeatureData = DataAnalysis().read_txt(abspath+"//data.txt")
    print attractionFeatureData[0]
    attractionSet = DataAnalysis().getAttraction(data)
    print len(attractionSet)
    resultList = DataAnalysis().getFeature(attractionFeatureData, attractionSet)
    print resultList
    DataAnalysis().writeMatrix(resultList,"changanjie.txt")

    
