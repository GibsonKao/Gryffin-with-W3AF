from selenium import webdriver
import time
import socket
from selenium.webdriver.common.by import By
import subprocess
import urlparse
import re 
import HTMLParser
import urllib2
import httplib

class GryffinRunner:

    def __init__(self,url):
        self.url=url

    def run(self):

        tsart1=time.time()

        gryffin_list=[]
        gryffinPath = "w3af/gryffin/render.js "

        f=open("result/"+self.url+"_W3afAnalyze.txt","r")
	griffinfd=open("result/"+self.url+"_GryffinOutput.txt","a")
        for i in f.readlines():
            i=i.strip()
            if i not in gryffin_list:
                gryffin_list.append(i)
        f.close()

        #old = len(gryffin_list)
        already=[]
        html_parser=HTMLParser.HTMLParser()
        for i in gryffin_list:
            if i not in already:
                already.append(i)
                try:
                    search = "phantomjs --ssl-protocol=any --ignore-ssl-errors=true --proxy=127.0.0.1:8080 --proxy-type=http "+gryffinPath+" "+i
                    process = subprocess.Popen(search.split(), stdout=subprocess.PIPE)
                except subprocess.CalledProcessError:
                    print "can not run gryffin"
                else:
                    output = process.communicate()[0].split('\n')
                    print str(output)
		    griffinfd.write(str(output))
                    for data in output:
                        check=0
                        data=html_parser.unescape(data)
                        grop=re.findall (r'http://[_:&-.A-Za-z0-9/]+',data)
                        for r in grop:
                            if r[-1]=="/":
                                url=r[:-1]
                            if url not in gryffin_list:
                                try:
                                    urllib2.urlopen(url)
                                except urllib2.HTTPError,e:
                                    print "HTTPError"
                                except urllib2.URLError,e:
                                    print "URLError"
                                except httplib.HTTPException:
                                    print "HTTPException"
                                else:
                                    gryffin_list.append(url)
                        grop2=re.findall (r'\.\./[_:&.A-Za-z0-9/-]+',data)
                        domain=urlparse.urljoin(i,'/')
                        for r in grop2:
                            url=domain+r[3:]
                            if url[-1]=="/":
                                url=url[:-1]
                            if url not in gryffin_list:
                                try:
                                    urllib2.urlopen(url)
                                except urllib2.HTTPError,e:
                                    print "HTTPError"
                                except urllib2.URLError,e:
                                    print "URLError"
                                except httplib.HTTPException:
                                    print "HTTPException"
                                else:
                                    gryffin_list.append(url)
                        grop3=re.findall (r'[/][_:&.A-Za-z0-9/-]+',data)
                        for r in grop3:
                            print "GROP3" 
                            if r[-1]=="/":
                                url=r[:-1]
                            if domain[-1]=="/":
                                domain=domain[:-1]
                            check=domain.rfind("/")
                            if check>=0:
                                print "domain = "+domain[check+1:]
                                abort=url.find(domain[check+1:])
                                if abort>=0:
                                    print "before url = "+url
                                    print "After abort"
                                    abort+=len(domain[check+1:])
                                    url=domain+url[abort:]
                                    print "after url = "+url
                                    print ""
                                else:
                                    url=domain+url
                            else:
                                url=domain+url
                            print url
                            if url not in gryffin_list:
                                try:
                                    urllib2.urlopen(url)
                                except urllib2.HTTPError,e:
                                    print "HTTPError"
                                except urllib2.URLError,e:
                                    print "URLError"
                                except httplib.HTTPException:
                                    print "HTTPException"
        			except ValueError:
                                    print "HTTPException"
                                else:
                                    print "ADD"
                                    print url
                                    gryffin_list.append(url)
        
        tend1=time.time()
        print "Time use = "+str(tend1-tsart1)
        f=open("result/"+self.url+"_urls.txt","w")
        #f.write("w3af = "+str(old)+"\n")
        #f.write("w3af+gryffin = "+str(len(gryffin_list))+"\n")
	set(gryffin_list)
        for i in gryffin_list:
            f.write(i)
            f.write("\n")
        f.close()
	griffinfd.close()
        print "GRYFFIN END\n"
