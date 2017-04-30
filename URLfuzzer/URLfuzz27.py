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
    if len(params) != 0:
        for payload in payloads:
            for param in params.keys():
                f.args[param] = payload.strip()
                Request(f.url.strip())
                f = furl(url)

#start threads for all requests
with open(sys.argv[1],'r') as f:
    urls = f.readlines()
    for u in urls:
        #use ? to identify urls with parameters
        if '?' in u:
            t = threading.Thread(target=buildRequest,args=(u,))
t.start()
