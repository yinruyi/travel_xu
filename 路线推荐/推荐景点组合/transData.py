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

class method():
    def transKind(self, kind):
        #print len(kind)
        result = {}
        direction = "ABCDEF"
        for i in xrange(len(kind)):
            temp = kind[i].split(",")
            for j in xrange(len(temp)):
                result[temp[j]] = direction[i]
        return result
    def transData(self,data):
        result = []
        for i in xrange(len(data)):
            temp = data[i].split(u",")
            result.append(temp)
        return result

    def getResult(self,data,kind):
        result  = []
        for i in xrange(len(data)):
            temp = data[i]
            if len(temp) > 0:
                result_temp = []
                for j in xrange(len(temp)):
                    if temp[j] == "":
                        pass
                    else:
                        result_temp.append(kind[temp[j]])
                result.append(result_temp)
        result = self.fixResult(result)
        return result

    def fixResult(self, dataset):
        result = []
        for i in xrange(len(dataset)):
            result_temp = []
            temp = dataset[i]
            if len(temp) == 1:
                result_temp = temp
            elif len(temp) > 1:
                result_temp.append(temp[0])
                for j in xrange(1,len(temp)):
                    if temp[j] == temp[j-1]:
                        pass
                    else:
                        result_temp.append(temp[j])
            result.append(result_temp)
        return result

    def getSmallResult(self, dataset, mainAttraction):
        result = []
        for i in xrange(len(dataset)):
            temp  = dataset[i]
            if len(temp) == 0:
                pass
            else:
                result_temp = []
                for j in xrange(len(temp)):
                    if temp[j] in mainAttraction:
                        result_temp.append(temp[j])
                if len(result_temp) != 0:
                    result.append(result_temp)
        return result



class DataAnalysis(pretreatment,method):
    def main(self):
        data = self.read_txt(abspath+"//998data.txt")
        data = self.transData(data)
        print data[0]
        kind = DataAnalysis().read_txt(abspath+"//kind.txt")
        kind = self.transKind(kind)
        print kind
        result = self.getResult(data, kind)
        print result
        self.writeMatrix(result,"ABCDEF.txt")

    def main1(self):
        data = self.read_txt(abspath+"//998data.txt")
        data = self.transData(data)
        print data[0]
        kind = DataAnalysis().read_txt(abspath+"//kind.txt")
        kind = self.transData(kind)
        #print kind
        direction = "ABCDEF"
        for i in xrange(len(kind)):
            temp = kind[i]
            print temp
            if len(temp) != 1:
                smallResult = self.getSmallResult(data, temp)
                print smallResult,len(smallResult)
            path = str(direction[i])+".txt"
            self.writeMatrix(smallResult,path)
            #break





if __name__ == '__main__':
    DataAnalysis().main1()
