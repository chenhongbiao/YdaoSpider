import requests

#this module want to direct anaylse the request and extract the notebook or note links
#but since the way used before, so i use Selenum "click" this time
def jumptopage(nod):
    url = "http://note.youdao.com/yws/mapi/readnote?method=hottestReadNote"
    headers = {"Accept":"*/*",
               "Referer":"http://note.youdao.com/dushu/web/index.html",
               "User-Agent":"Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36"
               }
    beginnum = (nod-1)*12
    params = {"begin":beginnum, "count":12} 
    req = requests.post(url, headers=headers, data=params)
    print(req.text)


jumptopage(65)