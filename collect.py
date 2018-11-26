import os
import time
import subprocess
import pexpect
import threading
from PreGryffin import Analyzer
from runGryffin import GryffinRunner
from runGryffin2 import GryffinRunner2
from AfterGryffin import W3afAgain

#PURPLE = '\033[95m'
#ENDC = '\033[0m'

def console(url):

    print ("W3af now using domain: " + url)
    child = pexpect.spawn('./w3af_console')
    #"^j" make a lot command fail in pexpect.py
    child.expect('w3af>>>')
    target = '\rtarget set target '+ url +'\r'
    print(target)
    child.sendline(target)
    #child.expect('w3af>>>')
    #child.sendline('\rplugins audit all\r')
    child.expect('w3af>>>')
    child.sendline('\rplugins crawl web_spider\r')
    child.expect('w3af>>>')
    child.sendline('\rplugins output text_file\r')
    child.expect('w3af>>>')
    child.sendline('\rplugins output config text_file\r')
    child.expect('w3af/plugins/output/config:text_file>>>')
    output = '\rset output_file result/' + url + '_W3afRaw.txt\r'
    print(output)
    child.sendline(output)
    child.expect('w3af/plugins/output/config:text_file>>>')
    child.sendline('\rview\r')
    child.expect('w3af/plugins/output/config:text_file>>>')
    child.sendline('\rback\r')
    child.expect('w3af>>>')
    child.sendline('\rstart\r')
    #some mysteries here, without some padding command, it will exit immediately.
    child.expect('w3af>>>')
    child.sendline('\rhelp\r')
    while(child.isalive()!=0):
        if(child.expect('w3af>>>',timeout=None)!=0):
    	    time.sleep(2)
    	else:
    	    break;
    child.sendline('\rexit\r')
    child.close()

def w3af(url):
    console(url)
    anlyz = Analyzer(url)
    anlyz.list_analyze()
    grfy = GryffinRunner(url)
    grfy.run()
    grfy2 = GryffinRunner2(url)
    grfy2.run()
    again = W3afAgain(url)
    again.looper()

if __name__ == "__main__":

    workdir = os.getcwd()
    if not os.path.exists(workdir+"/result"):
        os.system("mkdir result")

    with open("target.txt",'r') as txt:
        urls = [line.strip() for line in txt]

    threadList = []
    for u in urls:
        w3af(u)

