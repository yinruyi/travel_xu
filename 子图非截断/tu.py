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
		attractionList = []
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
			attractionList.append(attraction_temp)
			attraction.extend(attraction_temp)
		attractionSet = self.count(attraction)#景点名对应出现次数的set
		attractionList = self.clearAttraction(attractionList)#景点名二维list
		#print len(attractionSet)
		candidateConnection = self.calculateMC(attraction, attractionSet)#候选连接集
		#print candidateConnection[0:10]
		Connection = {}
		for i in xrange(len(candidateConnection)):
			temp = candidateConnection[i]
			#print temp[0],temp[1]
			num = 0#关系出现的次数
			for j in xrange(len(attractionList)):
				if temp[0] in attractionList[j] and temp[1] in attractionList[j]:
					num += 1
			#print num
			if num >= 10:
				mc = num/min(attractionSet[temp[0]],attractionSet[temp[1]])
				if mc >= 0.5:
					Connection[temp] = num

				
		print Connection,len(Connection)




	def calculateMC(self, attraction, attractionSet):
		attraction = list(set(attraction))
		candidateConnection = []
		for i in xrange(len(attraction)-1):
			for j in xrange(i+1,len(attraction)):
				if attractionSet[attraction[i]] >= 10 and attractionSet[attraction[j]] >= 10:
					candidateConnection.append((attraction[i],attraction[j]))
		return candidateConnection





	def up_supportAttraction(self, dataset, support = 10):
		dataset = self.count(dataset)
		pass




	def clearAttraction(self, dataset):
		attractionResult = []
		for i in xrange(len(dataset)):
			if len(dataset[i]) > 1:
				attractionResult.append(dataset[i])
		return attractionResult


class treatment():
	def count(self, dataset):
		resultSet = {}
		for i in xrange(len(dataset)):
			if dataset[i] in resultSet:
				resultSet[dataset[i]] += 1
			else:
				resultSet[dataset[i]] = 1
		return resultSet

	

		

		


class DataAnalysis(pretreatment, Methods, treatment):
	pass



if __name__=='__main__':
    data = DataAnalysis().read_txt(abspath+"//data//data.txt")
    mainAttraction = DataAnalysis().read_txt(abspath+"//data//mainAttraction.txt")
    DataAnalysis().getAttraction(data)
