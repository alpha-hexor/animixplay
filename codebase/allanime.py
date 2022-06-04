from .httpclient import HttpClient
from bs4 import BeautifulSoup as bs
from .extractor import *
import json
import re
import yarl
import os
from .gogoplay import extract_final_links

#Provider and their respective referrer
REFERRERS={
    'dood.to' : 'https://dood.to',
    'streamsb.net' : 'https://streamsb.net/',
    'ok.ru' : "",
    "mp4upload.com" : "https://mp4upload.com/",
    "goload.pro" : "https://gogoplay.io",
    "streamlare.com" : "https://streamlare.com"
}

#some global shit
req = HttpClient()
base_url = "https://animixplay.to"
mal_id = r"malid = '(\d+)'"

def al_extract_episode_info(isdub,anime_id):
    r=req.get(
        f"{base_url}/v1/{anime_id}"
    )
    
    mal=re.findall(mal_id,r.text)[0]
    
    r=req.post(
        f"{base_url}/api/search",
        data={
            "recomended" : mal
        },
        headers={
            'x-requested-with': 'XMLHttpRequest'
        }
    )
    
    data = json.loads(r.text)
    #print(data)
    try:
        for i in data["data"]:
            if i["type"] == "AL":
                a = [x["url"] for x in i["items"]]
        #print(a)
        try:
            anime_link = a[1] if isdub else a[1].split("-dub")[0]
        except:
            anime_link = a[0]
        r=req.get(
            f"{base_url}{anime_link}"
        )
        soup = bs(r.text,"html.parser")
        data = json.loads(soup.select("#epslistplace")[0].text)
        return data
    except:
        print("[*]Seems like the anime is not available")
        exit()


def al_return_link(link):
    """
     Args:
        link (str): pass to the extractors and return final streaming link and referrer
    """
    p_url =yarl.URL(link)
    
    if p_url.host == "dood.to":
        referrer = REFERRERS[p_url.host]
        link = dood(link)
        return referrer,link
    
    if p_url.host == "streamsb.net":
        referrer = REFERRERS[p_url.host]
        streamsb(link)
        #print(link)
        #print(f'mpv --http-header-fields="Accept-Language:en-US,User-Agent:Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.88 Safari/537.36" --referrer="{referrer}" "{link}"')
    
    if p_url.host == "ok.ru":
        referrer = REFERRERS[p_url.host]
        link = okru(link)
        return referrer,link

    if p_url.host == "mp4upload.com":
        referrer = REFERRERS[p_url.host]
        link = mp4upload(link)
        return referrer,link
    
    if p_url.host == "goload.pro":
        from_al = True
        #referrer = REFERRERS[p_url.host]
        link = extract_final_links(from_al,f"https:{link}")
        print(link)
        #os.system(f"mpv --referrer={referrer} {link}")
        
        #return referrer,link
        
    if p_url.host == "vidstream.io":
        print("[*]Sorry not impleamneted yet")
        exit()
        
    if p_url.host == "streamlare.com":
        referrer = REFERRERS[p_url.host]
        link = streamlare(link)
        return referrer,link