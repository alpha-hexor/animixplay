'''
python code to parse m3u8 quality
'''

from tkinter.messagebox import NO
from .httpclient import HttpClient
import regex
import re
import yarl

requests = HttpClient()

#regex 
start_regex = regex.compile(r"#EXT-X-STREAM-INF(:.*?)?\n+(.+)")
res_regex = regex.compile(r"RESOLUTION=\d+x(\d+)")

def fix_link(link):
    #fix for gogoanime and asianembed links
    RE_URL_IS = r"(?<=\/)http[s]?:\/\/(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+"
    return re.search(RE_URL_IS, link).group(0)    


def get_m3u8_quality(link):
    #print("i got called")
    links = []
    qualities = []
    
    partial_link = link[:link.rfind('/')+1]
    
    r=requests.get(link)
    
    
    
    for i in start_regex.finditer(r.text):
        res_line,l = i.groups()
        
        #construct the quality 
        qualities.append(str(res_regex.search(res_line).group(1))+"p")
        #print(qualities)
        #construct link
        if yarl.URL(str(l.strip())).is_absolute():
            links.append(str(l.strip()))
        else:
            link=partial_link+l.strip()
            if len(re.findall("https://",link)) > 1:
                    links.append(fix_link(link))
            else:
                links.append(link)
    if "manifest.prod" in yarl.URL(link).host:
        print("[*]Audio got called")
        audio = re.findall(r'URI="(.*?)"',r.text)[0]
    else:
        print("[*]Audio did not get called")
        audio = None
        
    return audio,qualities,links

    