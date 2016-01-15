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


		

class DataAnalysis(pretreatment, Methods):
    pass



if __name__=='__main__':
    dataset = DataAnalysis().read_txt(abspath+'//998data.txt')
    dataset = DataAnalysis().makeMatrix(dataset)
    #print dataset[0]
    scence = DataAnalysis().getScence(dataset)
    print scence,len(scence)