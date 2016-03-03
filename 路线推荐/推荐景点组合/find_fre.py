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
            temp = " ".join(temp)
            dataset[i] = temp
        string = "\n".join(dataset)
        f = open(Path, "a+")
        line = f.write(string+"\n")
        f.close()

class method():
    def read_data(self,path):
        result = []
        data = self.read_txt(path)
        for i in xrange(len(data)):
            temp = data[i].split(u",")
            temp = list(set(temp))
            result.append(temp)
        return result

    def attractionFP(self, dataset):
        #对景点挖掘频繁集
        resultSet = {}
        resultList = []
        for i in xrange(len(dataset)):
            #print "DDDDDDDDDDDDDDDD"
            temp = dataset[i]
            if len(resultList) == 0:
                resultSet[tuple(temp)] = 1
                resultList.append(temp)
                #print "OOOOOOOOOOOOo"
            else:
                #print "SSSSSSSSSSSS"
                flag = 0
                for j in xrange(len(resultList)):
                    #print "DD"
                    if set(resultList[j]) == set(temp):
                        temp = resultList[j]
                        flag = 1
                        #print "kkk"
                if flag == 0 :
                    resultList.append(temp)
                    resultSet[tuple(temp)] = 1
                else:
                    #print "KKK"
                    resultSet[tuple(temp)] += 1
        return resultSet

class DataAnalysis(pretreatment,method):
    def main(self):
        data = self.read_data("D.txt")
        print data[0],len(data)
        dataFP = self.attractionFP(data)
        #print dataFP,len(dataFP)
        result2write = []
        for k,v in dataFP.items():
            #print k,v
            temp = list(k)
            temp.append(v)
            result2write.append(temp)
            #if v == 487:
            #    print k ,"QQQQQQQQ"
            #elif v>487:
            #    print k,v,"!!!!!"
        self.writeMatrix(result2write,"result.txt")


if __name__ == '__main__':
    DataAnalysis().main()