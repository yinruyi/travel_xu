#coding:utf-8
import sys
import os

reload(sys)
sys.setdefaultencoding('utf-8')
abspath = os.getcwd()

class pretreatment():
    """预处理"""
    def __init__(self):
        pass
    def read_txt(self,txtPath,coding = 'utf-8'):
        import codecs
        f = codecs.open(txtPath,'r',coding).readlines()
        f[0] = f[0].replace(u"\ufeff",u"")
        dataset = []
        for line in f:
            line = line.replace(u"\r\n",u"")
            line = line.replace(u"\n",u"")
            dataset.append(line)
        return dataset

    def test():
    	pass


class DataAnalysis(pretreatment):
    pass



if __name__=='__main__':
    data = DataAnalysis().read_txt(abspath+'//data//beijing_attraction.txt')
    data = DataAnalysis
    print data