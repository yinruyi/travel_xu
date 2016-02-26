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
    def getseqmian(self, data,city,rounte):
        #print data[0]
        data = self.word_tag_fliter(data)
        data = self.tab_flitter(data,8)
        print data[0]
        data = self.scence(data)
        print data[0]

    def scence(self,data):
        #非热门景点标记成kkkkkk
        scence = self.read_txt(abspath+"//data//mainAttraction.txt")#景点矩阵
        for i in range(len(data)):
            temp = data[i].split('******')
            if len(temp) > 0:
                for j in range(len(temp)):
                    h = temp[j].split()
                    if len(h) > 0:
                        for k in range(len(h)):
                            aa = h[k].split('/')
                            if len(aa) == 2:
                                if aa[1] == 'tttttttt' and aa[0] not in scence:
                                    h[k] = '/'.join([aa[0],'kkkkkk'])
                    temp[j] = ' '.join(h)
            data[i] = ' ****** '.join(temp)
        return data

class treatment():
    def treat(self, dataset):
        #print dataset[0]
        dataset = self.word_tag_fliter(dataset)
        #print dataset[0]
        dataset = self.maketuple(dataset)
        #print dataset[0]
        dataset = self.beforecount(dataset)
        #print dataset[0:100]
        dataset_count = self.counts(dataset)
        dataset_count['******'] = 0
        return dataset_count


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

    def maketuple(self, data):
        #将元组中每行删去重复的
        new_data = []
        for i in range(len(data)):
            temp = data[i].split()
            if len(temp) == 1:
                new_data.append(temp)
            else:
                if len(temp) > 1:
                    new_temp = []
                    for j in range(len(temp)):
                        if temp[j] not in new_temp:
                            new_temp.append(temp[j])
                    new_data.append(new_temp)
        return new_data

    def beforecount(self, data):
        new_data = []
        for i in range(len(data)):
            temp = data[i]
            if len(temp) >= 1:
                for j in range(len(temp)):
                    new_data.append(temp[j])
        for i in range(len(new_data)):
            temp = new_data[i].split('/')
            new_data[i] = temp[0]
        return new_data
            
    def counts(self, data):
        dic = {}
        for i in range(len(data)):
            if data[i] in dic:
                dic[data[i]] += 1
            else:
                dic[data[i]] = 1
        return dic

    def tab_flitter(self,data,num):
        #过滤空行
        new_data = []
        for i in range(len(data)):
            if len(data[i]) <= num:
                pass
            else:
                new_data.append(data[i])
        return new_data

class DataAnalysis(pretreatment, Methods, treatment):
	pass



if __name__=='__main__':
    data = DataAnalysis().read_txt(abspath+"//data//data.txt")
    mainAttraction = DataAnalysis().read_txt(abspath+"//data//mainAttraction.txt")
    dataset_count = DataAnalysis().treat(data)
    #print "aa"
    #print type(data),data[0]
    for i in xrange(len(mainAttraction)):
        rounte = str(mainAttraction[i])+".txt"
        print mainAttraction[i],rounte
        DataAnalysis().getseqmian(data,mainAttraction[i],rounte)
        break

