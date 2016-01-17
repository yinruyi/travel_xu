#coding:utf-8

import os
import sys
import string
import codecs
import numpy as np
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
    def makeMatrix(self, dataset):
    	for i in xrange(len(dataset)):
    		temp = dataset[i].split()
    		dataset[i] = temp
    	return dataset

def writeMatrix(dataset, Path, coding = "utf-8"):
	for i in xrange(len(dataset)):
		temp = dataset[i]
		temp = [str(temp[j]) for j in xrange(len(temp))]
		temp = ",".join(temp)
		dataset[i] = temp
	string = "\n".join(dataset)
	f = open(Path, "a+")
	line = f.write(string+"\n")
	f.close()

class Methods(object):
	"""docstring for Methods"""
	def __init__(self, arg):
		super(Methods, self).__init__()
		self.arg = arg
	def getScence(self, dataset):
		scence = []
		for i in xrange(len(dataset)):
			temp = dataset[i]
			if len(temp) == 0:
				pass
			else:
				for j in xrange(len(temp)):
					singleWord = temp[j].split(u"/")
					if len(singleWord) == 2:
						if singleWord[1] == "tttttttt":
							scence.append(singleWord[0])
		scence = list(set(scence))
		return scence
	def getHITSMatrix(self, dataset, scence):
		#print dataset[0]
		arr = []
		for i in xrange(len(dataset)):
			#print dataset[i]
			seq = []
			for j in xrange(len(scence)):
				if scence[j] in dataset[i]:
					seq.append(1)
				else:
					seq.append(0)
			#print seq
			arr.append(seq)
		return np.array(arr)
	def hits(self, x, dataset, scence):
		result = []
		J = []#景点
		U = []#游客
		j = np.ones((len(scence),1))
		J.append(j)
		u = np.ones((len(dataset),1))#初始化
		U.append(u)
		k = 1
		while k > 0.001:
			u = np.dot(x,j)/max(np.dot(x,j))
			j = np.dot(x.T,u)/max(np.dot(x.T,u))
			k = sum(U[-1]-u)+sum(J[-1]-j)
			J.append(j)
			U.append(u)
		for item in xrange(len(j)):
			#print j[item]
			result.append(list(j[item])[0])
			#break
		return result


		

class DataAnalysis(pretreatment, Methods):
    pass



if __name__=='__main__':
    dataset = DataAnalysis().read_txt(abspath+'//998data.txt')
    #print dataset_original[0]
    dataset = DataAnalysis().makeMatrix(dataset)
    #print dataset[0]
    scence = DataAnalysis().getScence(dataset)
    #print scence,len(scence)
    hitsMatrix = DataAnalysis().getHITSMatrix(DataAnalysis().read_txt(abspath+'//998data.txt'), scence)
    #print hitsMatrix[0]
    scence_point = DataAnalysis().hits(hitsMatrix, dataset, scence)
    resultList = [[scence[i],scence_point[i]] for i in xrange(len(scence))]
    print resultList[0]
    writeMatrix(resultList,"result.txt")