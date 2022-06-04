'''
python code to parse m3u8 quality
'''

from .httpclient import HttpClient
import regex
import re

requests = HttpClient()

#regex 
start_regex = regex.compile(r"#EXT-X-STREAM-INF(:.*?)?\n+(.+)")
res_regex = regex.compile(r"RESOLUTION=\d+x(\d+)")

def fix_link(link):
    #fix for gogoanime and asianembed links
    RE_URL_IS = r"(?<=\/)http[s]?:\/\/(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+"
    return re.search(RE_URL_IS, link).group(0)    


def get_m3u8_quality(link):
    
    links = []
    qualities = []
    
    partial_link = link[:link.rfind('/')+1]
    
    r=requests.get(link)
    
    
    for i in start_regex.finditer(r.text):
        res_line,l = i.groups()
        
        #construct the quality 
        qualities.append(str(res_regex.search(res_line).group(1))+"p")
        
        #construct link
        link=partial_link+l.strip()
        if len(re.findall("https://",link)) > 1:
                links.append(fix_link(link))
        else:
            links.append(link)
    
    return qualities,links

    