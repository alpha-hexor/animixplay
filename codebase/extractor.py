#list of extractors for allanime
from .httpclient import HttpClient
from bs4 import BeautifulSoup as bs
import re
import json
import time
import yarl
from html import unescape
import jsbeautifier
from colorama import Fore, Style

#global shit goes here
req = HttpClient()
dood_md5_regex = r"/(pass_md5/.+?)'"
strem_sb_payload = "76594275494f6a424d6852687c7c{}7c7c724f6c6453373351356f64457c7c73747265616d7362/5641576b747a61674f4a6d617c7c346334323737333237373465363234643633373535363761376337633436333036313636353133353436346336623438346637353763376333393635366536343638346235383632343235613531353037633763373337343732363536313664373336327c7c6474336d6e556e7879446a697c7c73747265616d7362"
streamsb_id_regex = r"/e/([^?#&/.]+)"
ok_ru_regex = r'data-options="([^"]*)"'
player_src_regex = r"player\.src\(([^)]+)\)"

#color shit
red = lambda a: f"{Fore.RED}{a}{Style.RESET_ALL}"

#doodstream
def dood(link):
    #print(link)
    r=req.get("https://check.ddos-guard.net/check.js").text
    r=req.get(link)
    #print(r.text)
    try:
        hash = re.findall(dood_md5_regex, r.text)[0]
    except:
        print(red("[*]Seems like doodstream link is not available"))
        exit()
    token = hash.split("/")[-1]
    r=req.get(f"https://dood.to/{hash}",headers={"Referer":"https://dood.to"})
    link = f"{r.text}doodstream?token={token}&expiry={int(time.time() * 1000)}"
    return link
    
#streamsb
    """
    Not functional
    """
def streamsb(link):
    #print(link)
    stream_id = re.findall(streamsb_id_regex, link)[0]
    url = f"https://{yarl.URL(link).host}/"
    print(url)
    sources = req.get(
        url +"sources43/{}".format(
            strem_sb_payload.format(stream_id.encode().hex())),
            
    
        headers={
            "watchsb": "streamsb",
            "referer": link,
        }
    ).json().get("stream_data",{})
    #print(sources)
    r=req.get(sources.get("file"),
              headers={
                  "Referer": url,
              })
    print(r.text)

#ok.ru
def okru(link):
    ru_id = link.split("/")[-1]
    url = f"https://odnoklassniki.ru/videoembed/{ru_id}"
    r=req.get(url).text
    try:
        data = json.loads(
            unescape(re.findall(ok_ru_regex, r)[0])
        ).get("flashvars", {}).get("metadata")
        
        return json.loads(data).get("hlsManifestUrl")
    except:
        print(red("[*]Ok.ru is blocked"))
        exit()
    
#mp4upload
def mp4upload(link):
    r=req.get(link,headers={
        "DNT": "1"
    }).text
    soup = bs(r, "html.parser")
    try:
        x = jsbeautifier.beautify(soup.select("script")[-3].text)
        return re.findall(player_src_regex, x)[0]
    except:
        print(red("[*]Mp4upload is blocked"))
        exit()
    
#streamlare
def streamlare(link):
    stream_id = link.split("/")[-1]
    
    #collect the csrf token
    r=req.get(link).text
    soup = bs(r, "html.parser")
    csrf_token = soup.select("meta[name=csrf-token]")[0].get("content")
    
    r=req.post(
        "https://streamlare.com/api/video/download/get",
        
        data={"id":stream_id},
        
        headers={
            "x-requested-with":"XMLHttpRequest",
            "x-csrf-token" : csrf_token,
        }
        
        
    ).json()
    return r.get("result",{}).get("Original",{}).get("url")