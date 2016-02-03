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

class treatment():
	def count(self, dataset):
		resultSet = {}
		for i in xrange(len(dataset)):
			if dataset[i] in resultSet:
				resultSet[dataset[i]] += 1
			else:
				resultSet[dataset[i]] = 1
		return resultSet

	def learnLinkList(self, dataset):
		linkList = []
		for i in xrange(len(dataset)):
			temp = dataset[i]
			if len(temp) == 2:





class Methods():
	def getAttraction(self, dataset):
		#找寻TOP30-50热门景点
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
					if len(item) == 2 and item[1] == "tttttttt":
						attraction_temp.append(item[0])
						#print attraction_temp
			attraction_temp = list(set(attraction_temp))
			attraction.extend(attraction_temp)
		#print "hh"
		#print attraction
		print len(list(set(attraction)))
		attractionCount = self.count(attraction)
		print attractionCount
		attractionList = []
		for k,v in attractionCount.items():
			temp = [k,v]
			attractionList.append(temp)
			#print attractionList
			#break
		self.writeMatrix(attractionList,"result.txt")



	def getmainAttractionLink(self, dataset, mainAttraction):
		#找出大景区
		candidateLink = []
		attractionLink = []
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
					if len(item) == 2 and item[1] == "tttttttt":
						attraction_temp.append(item[0])
						#print attraction_temp
			attraction_temp = list(set(attraction_temp))
			attractionLink.append(attraction_temp)
			attraction.extend(attraction_temp)
		#print attractionLink[2],len(attractionLink)
		attractionCount = self.count(attraction)


class test():
	def test():
		pass
		

class DataAnalysis(pretreatment, Methods, treatment, test):
	pass



if __name__=='__main__':
    data = DataAnalysis().read_txt(abspath+"//data//data.txt")
    #print data[0]
    #DataAnalysis().getAttraction(data)
    mainAttraction = DataAnalysis().read_txt(abspath+"//data//mainAttraction.txt")
    #print mainAttraction
    DataAnalysis().getmainAttractionLink(data, mainAttraction)