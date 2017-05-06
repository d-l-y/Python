import requests
from furl import furl
import threading
import sys

payloads = open('payloads.txt','r').readlines()
reflections = open('reflections.txt','r').readlines()

#kill warnings about bad certs
requests.packages.urllib3.disable_warnings()

#function to request the url with payload and parse for reflection
def Request(url):
    global reflections
    global queueCount

    try:
        r = requests.get(url.strip(),verify=False,timeout=20)
        pageContent = r.content
        responseTime = r.elapsed.total_seconds()
        responseLength = len(pageContent)
        code = r.status_code

        #if the response code is not 404 or 403 and a payload is reflected, print it out.
        if code not in [404,403]:
            for string in reflections:
                if string.strip() in pageContent:
                    print '[+] '+string.strip()+' reflected in '+url.strip()
                    
    #continue even if there are errors with request
    except:
        pass

#function to create the url with current payload and start request    
def buildRequest(url):
    global payloads
    f = furl(url)
    params = f.args
    for payload in payloads:
        for param in params.keys():
            f.args[param] = payload.strip()
            Request(f.url.strip())
            f = furl(url)

#start threads for all requests
with open(sys.argv[1],'r') as f:
    urls = f.readlines()
    reqList = []
    for u in urls:
        #check if URL has parameters and only start threads on unique URLs
        f = furl(u)
        if len(f.args) != 0:
            for p in f.args.keys():
                f.args[p] = ''
            if f.url not in reqList:
                reqList.append(f.url)
                t = threading.Thread(target=buildRequest,args=(u,))
                t.start()
