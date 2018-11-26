import os

class Analyzer:
    def __init__(self, url):
        self.url = url

    def list_analyze(self):
        try:
            fin=open("result/"+self.url+"_W3afRaw.txt","r")
	    f=open("result/"+self.url+"_W3afAnalyze.txt","w")
        except (IOError,OSError) as e:
            print "\n"+line+".txt don't exist."
        else:
            print ""
            url_start=0
            url_count=0
            url_total=0
            inject_start=0
            inject_count=0
            inject_total=0
	    W3af_list=[]
            for infor in fin.readlines():
                infor=infor.strip()
                if url_start==0:
                    start = infor.find("information] Found")+19
                    if(start>=19):
                        end = infor.find(" URLs",start)
                        url_total = int(infor[start:end])
                        url_start=-1
                        start = infor.find("and ",end)+4
                        if(start>=4):
                            end = infor.find(" different injections",start)
                            inject_total=int(infor[start:end])
                            inject_start=-1
                elif url_start==-1:
                    if (infor.find("The URL list is")>=0):
                        url_start=1
                elif url_start==1 and url_count<url_total:
                    start = infor.find("information] ")+14
                    if(start>=14):
                        url_count+=1
                        #cwd=os.getcwd()+"/result/"
                        #file_path=os.path.join(cwd+"/gryffin","w3af_output_urls.txt")
                        #file_path=os.path.join(cwd,self.url+"_W3afAnalyze.txt")
                        #f_out=open(file_path,"a")
                        #f_out=open("456.txt","a")
			W3af_list.append(infor[start:])
                        #f_out.write(infor[start:])
                        #f_out.write("\n")
                        #f_out.close()
                elif url_start==1 and inject_start==-1:
                    if (infor.find("The list of fuzzable requests")>=0):
                        inject_start=1

                #elif inject_start==1 and inject_count<inject_total:
                    #start = infor.find("information] ")+14
                    #if(start>=14):
                        #inject_count+=1

                else:
                    pass
            fin.close()
	    set(W3af_list)
	    for i in W3af_list:
	        f.write(i)
		f.write("\n")
	    f.close()
	    print "There are "+str(url_count)+" urls"
            #print "There are "+str(inject_count)+" fuzzable requests"

