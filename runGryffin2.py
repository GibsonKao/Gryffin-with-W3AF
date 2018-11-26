from selenium import webdriver
from bs4 import BeautifulSoup
from bs4 import Comment
import time
import socket
from selenium.webdriver.common.by import By
import subprocess
import urlparse
import re 
import HTMLParser
import urllib2
import httplib
from urlparse import urljoin

class GryffinRunner2:

    protocols = ('http', 'https')
    extensions = ('.php', '.htm', '.html', '.asp', '.cgi')


    def __init__(self,url):
        self.url=url

    def _get_domain_name(self, url):
        
        if re.match('http://|https://', url):
            # print 'match http ' + url
            result = urlparse.urlparse(url)
            return result.scheme + '://'+result.netloc

    def _is_url_connectable(self, url):
        try:
            urllib2.urlopen(url)
        except urllib2.HTTPError,e:
            print "HTTPError"
            return False
        except urllib2.URLError,e:
            print "URLError"
            return False
        except httplib.HTTPException:
            print "HTTPException"
            return False
        except ValueError:
            print "ValueError"
            return False
        else:
            return True

    def _show_links(self, lists):
        index = 1
        for link in lists:
            print ("%d %s" % (index, link))
            index += 1 

    def run(self):

        t_start = time.time()

        gryffin_list=[]
        urls_list_set = set()
        gryffinPath = "w3af/gryffin/render.js "

        # f=open("result/"+self.url+"_W3afAnalyze.txt","r")
        f=open("result/"+self.url+"_urls.txt","r")
        griffinfd=open("result/"+self.url+"_GryffinOutput2.txt","a")
        for i in f.readlines():
            i=i.strip()
            if i not in gryffin_list:
                gryffin_list.append(i)
                urls_list_set.add(i)
        f.close()

        already_parsed = set()
        html_parser=HTMLParser.HTMLParser()
        
        found_links = []
        
        ### parsed the urls from W3AF
        for url in urls_list_set:

            if url not in already_parsed:
                already_parsed.add(url)
                domain_name = self._get_domain_name(url)

            try:
                search = "phantomjs --ssl-protocol=any --ignore-ssl-errors=true --proxy=127.0.0.1:8080 --proxy-type=http "+gryffinPath+" "+ url
                process = subprocess.Popen(search.split(), stdout=subprocess.PIPE)
            except subprocess.CalledProcessError:
                print "can not run gryffin"
            else:
                response = process.communicate()
                response_text = str(response)

                ### 1st, parsing the http response
                response_split = response_text.split(",")
                for item in response_split:
                    if item.startswith("\"url\""):
                        pairs = item.split("\"")
                        for value in pairs:
                            if value.startswith(self.protocols):
                                if "?" in value:
                                    tmp = value.split("?")
                                    value = tmp[0]

                                if value not in found_links:
                                    if self._is_url_connectable(value):
                                        found_links.append(value)

                ### 2nd, for url in comment
                soup=BeautifulSoup(response_text,'html.parser')
                comments=soup.find_all(string=lambda text:isinstance(text,Comment))
                for comment in comments:
                    comment_split = comment.split(" ")
                    for value in comment_split:
                        if value.startswith(self.protocols):
                            if value not in found_links:
                                if self._is_url_connectable(value):
                                    found_links.append(value)
                        elif value.endswith(self.extensions):
                            
                            if value.startswith(self.url):
                                value = "http://" + value
                            elif value.startswith("/"):
                                value = "http://" + self.url + value
                            else :
                                value = "http://" + self.url + "/"+value

                            print value

                            if value not in found_links:
                                if self._is_url_connectable(value):
                                    found_links.append(value)


        ### show the parsed result
        self._show_links(found_links)

        f=open("result/"+self.url+"_urls.txt","w")
        for i in found_links:
            f.write(i)
            f.write("\n")
        f.close()
        griffinfd.close()

        ### print excuted time ###
        t_end = time.time()
        hours, rem = divmod(t_end - t_start, 3600)
        minutes, seconds = divmod(rem, 60)
        print("executed {:0>2}:{:0>2}:{:05.2f}".format(int(hours),int(minutes),seconds))