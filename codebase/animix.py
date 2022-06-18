from .httpclient import HttpClient
from bs4 import BeautifulSoup as bs
from .extractor import *
import yarl
from .gogoplay import extract_final_links
from colorama import Fore, Style



#some global shit
req = HttpClient()
base_url = "https://animixplay.to"
URL_REGEX = r'(?:(?:https):\/\/)?[\w/\-?=%.]+\.[\w/\-&?=%.]+'

red = lambda a: f"{Fore.RED}{a}{Style.RESET_ALL}"
    
def generate_link(link):
    '''
    function to return final streaming link
    '''
    x =link.split("##")
    if len(x) >= 1:
        #use the first one if multiple links are found
        l = x[0]
   
    #huge try and except block
    

    if yarl.URL(l).host == "www.dailymotion.com":
       
        return dailymotion(l)
        
    elif yarl.URL(l).host == "ok.ru":
        return okru(l)
        
    elif yarl.URL(l).host == "goload.pro":
        link = animixplay_link(l)
        if not link:
            link = extract_final_links(True,l)
        return link
        
    
    else:    #for adult animes
        link =  decode_from_base64(l)
        if not link:
            print(red("[*]Seems like link is not available"))
            exit()
        return link
            
        
    
    
        