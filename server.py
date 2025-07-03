import http.server
import sys
import os
import json
import threading
import time
import urllib
import urllib.request

path = os.path.abspath(sys.argv[1])
os.makedirs(path, exist_ok=True)

pool = []
poolLock = threading.Lock()


class cServer(http.server.SimpleHTTPRequestHandler):
    def do_POST(self):
        global pool

        data = json.loads(self.rfile.read(
            int(self.headers["Content-Length"])
        ).decode("utf-8"))
        
        with poolLock:
            pool += data["content"]
 
class cDownloader:

    def serve_forever(self):
        while True:
            time.sleep(0.2)
            
            with poolLock:
                if pool:
                    #process url
                    url = urllib.parse.urlparse(pool.pop(0))
                    query = urllib.parse.parse_qs(url.query)
                    query["name"] = "large" #biggest resolution
                    fext = query["format"] = query["format"][0]
                    link = url._replace(query=urllib.parse.urlencode(query)).geturl()
                    
                    #render path
                    name = os.path.basename(url.path)
                    filename = f"{name}.{fext}"
                    filepath = os.path.join(path, filename)

                    print(f"({len(pool)}) {link} => {filepath} ... ", end="")

                    #download
                    if (not os.path.exists(filepath)):
                        try:
                            opener = urllib.request.build_opener()
                            opener.addheaders = [('User-agent', 'Mozilla/5.0')]
                            urllib.request.install_opener(opener)
                            urllib.request.urlretrieve(link, filepath)

                        except urllib.error.HTTPError:
                            print("failed")

                    print("done")

bind = ("127.0.0.1", 5000)
xServer = http.server.HTTPServer(bind, cServer)
xDownloader = cDownloader()



threading.Thread(target = lambda:     xServer.serve_forever(), daemon=True).start()
threading.Thread(target = lambda: xDownloader.serve_forever(), daemon=True).start()

try:
    while True:
        time.sleep(0.1)
        
except KeyboardInterrupt:
    pass
        
        
        
