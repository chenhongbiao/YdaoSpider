from urllib.request import urlopen
from urllib.parse import urlparse
import json
import re
from bs4 import BeautifulStoneSoup



#get a notebook url (shareKey or shareId) and return a list of note links
def getNoteLinks(bookurl):
    shrquery = urlparse(bookurl).query
    #scheme://netloc/path;parameters?query#fragment.
    shareKey = shrquery.replace("id=", "").split("&")[0]
    notejson = "http://note.youdao.com/yws/public/notebook/"+shareKey
    njson = urlopen(notejson)
    njson = str(njson.read(),"utf-8")

    #noteids = re.findall(shareKey+'/WEB[a-zA-Z0-9]*/WEB',njson)
    #okay, okay, the regex is really powerful and really hard to control
    
    #it need to be cut one more "},{" but it would be ugly, so use regex
    #dirty skills, don't do this at home = -= #cut the string make it like the json standard file
    #num = njson.split("[")[1].split(",")[0]
    #print(int(num))
    njson = njson.split("[")[2].split("]")[0]
    jsonparts = njson.split("},{")
    #the powershell print is fuck off, but the result is correct.
    notelinks = []
    index = 0
    for jsonpart in jsonparts:
        if (index==0):
            jsonpart = jsonpart+"}"
        elif (index == len(jsonparts)-1):
            jsonpart = "{" + jsonpart
        else:
            jsonpart = "{" + jsonpart + "}"
        jsobj = json.loads(jsonpart)
        noteid = urlparse(jsobj.get("pp")["thmurl"]).path.split("/")[5]
        notelinks.append("http://note.youdao.com/share/?id="+shareKey+"&type=notebook#/" +noteid)
        index +=1
    return notelinks

notelinks = getNoteLinks("http://note.youdao.com/share/?id=81c26805eb409c777f75ab97ad5335f8&type=notebook")
print(len(notelinks))
for notelink in notelinks:
    print(notelink)