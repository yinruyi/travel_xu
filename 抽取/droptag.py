


if __name__=='__main__':
    rounte = '中环.txt'
    data = open(rounte,'r',encoding= 'utf-8').readlines()
    for i in range(len(data)):
    	a = data[i].split()
    	if len(a) > 0:
    		for j in range(len(a)):
    			kk = a[j].split('/')
    			if len(kk) == 1:
    				pass
    			elif len(kk) == 2:
    				a[j] = kk[0]
    			else:
    				a[j] = ' '
    	data[i] = ' '.join(a)
    write_file=open(rounte,'w',encoding= 'utf-8')
    for i in range(len(data)):
        write_file.writelines(data[i])
        write_file.writelines('\n')
    write_file.close()

