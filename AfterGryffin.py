import os
import pexpect
import re

class W3afAgain:
    def __init__(self, url):
        self.url = url

    def looper(self):
        os.system("mkdir result/audit")
        os.system("mkdir result/audit/raw")
        os.system("mkdir result/audit/html")
        os.system("mkdir result/audit/csv")
        os.system("mkdir result/audit/xml")

        print self.url

        try:
            fin=open("result/"+self.url+"_urls.txt","r")
        except (IOError,OSError) as e:
            print "\n"+line+".txt don't exist."
        else:
            for line in fin.readlines():
                line = line.strip()
                if self.url in line:
                    print line
                    self.expector(line)
	    print ("looper now finished!! ")

    def expector(self, url):
        print ("W3af now using domain: " + url)
        child = pexpect.spawn('./w3af_console')
        #"^j" make a lot command fail in pexpect.py
        child.expect('w3af>>>')
        target = '\rtarget set target '+ url +'\r'
        print(target)
        child.sendline(target)
        # child.expect('w3af>>>')
        child.sendline('\rplugins audit all\r')
        #child.expect('w3af>>>')
        #child.sendline('\rplugins crawl web_spider\r')


        ########Done########
        # - Enable the html_file and csv_file
        # - must set the file name and path
        #####################


        child.expect('w3af>>>')
        child.sendline('\rplugins output text_file html_file csv_file xml_file\r')
        child.expect('w3af>>>')
        
        ########Done########
        # - The file name can not contain / <-- it will be regonize an directory in the path
        # - fix the url name
        #####################
        filename = re.sub(r"/", "-", url)
        print filename

        ## raw text
        child.sendline('\rplugins output config text_file\r')
        child.expect('w3af/plugins/output/config:text_file>>>')
        output = '\rset output_file result/audit/raw/' + filename + '_raw.txt\r'
        child.sendline(output)
        child.expect('w3af/plugins/output/config:text_file>>>')
        child.sendline('\rback\r')

        ## html file               
        child.sendline('\rplugins output config html_file\r')
        child.expect('w3af/plugins/output/config:html_file>>>') 
        output = '\rset output_file result/audit/html/' + filename + '.html\r'
        child.sendline(output)
        child.expect('w3af/plugins/output/config:html_file>>>') 
        child.sendline('\rback\r')


        ## csv file
        child.sendline('\rplugins output config csv_file\r')
        child.expect('w3af/plugins/output/config:csv_file>>>') 
        output = '\rset output_file result/audit/csv/' + filename + '.csv\r'
        child.sendline(output)
        child.expect('w3af/plugins/output/config:csv_file>>>') 
        child.sendline('\rback\r')

        ## xml file
        child.sendline('\rplugins output config xml_file\r')
        child.expect('w3af/plugins/output/config:xml_file>>>') 
        output = '\rset output_file result/audit/xml/' + filename + '.xml\r'
        child.sendline(output)
        child.expect('w3af/plugins/output/config:xml_file>>>') 
        child.sendline('\rback\r')
        

        ##############################################
        ### perform testing
        ##############################################
        child.expect('w3af>>>')
        child.sendline('\rstart\r')
        #some mysteries here, without some padding command, it will exit immediately.
        child.expect('w3af>>>')
        child.sendline('\rhelp\r')
        while(child.isalive()!=0):
            if(child.expect('w3af>>>',timeout=None)!=0):
                time.sleep(2)
            else:
                break
        child.sendline('\rexit\r')
        child.close()


