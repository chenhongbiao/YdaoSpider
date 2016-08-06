from bs4 import BeautifulSoup
from urllib.parse import urlparse

def getBnoteLinks(bsObj):
    #Collects all internal notebook or note links in home page - the rank hot part
    allbookLinks = set()
    allnoteLinks = set()
    
    #ul id=main-list  li class="note-item"
    for noteItem in bsObj.find("ul",{"id":"main-list"}).findAll("li",{"class":"note-item"}):
        noteItemLink = noteItem.find("a").attrs["href"]
        Linkparts = urlparse(noteItemLink).query.replace("id=", "").split("&")
        if(Linkparts[1] == "type=note"):
            allnoteLinks.add("http://note.youdao.com/share/?id="+Linkparts[0]+"&type=note")
        elif(Linkparts[1]=="type=notebook"):
            allbookLinks.add("http://note.youdao.com/share/?id="+Linkparts[0]+"&type=notebook")
            
    for booklink in allbookLinks:
        print(booklink)
    for notelink in allnoteLinks:
        print(notelink)
    return allnoteLinks, allbookLinks

if __name__ == "__main__":
    print("You ran this module directly (and did not 'import' it).")