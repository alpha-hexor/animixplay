from .httpclient import HttpClient
from .extractor import *
import yarl
from .gogoplay import extract_final_links
from colorama import Fore, Style
from .ui import *



#some global shit
req = HttpClient()
base_url = "https://animixplay.to"


    
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
        
    elif yarl.URL(l).host == "goload.pro" or yarl.URL(l).host == "gogohd.net":
        data = animixplay_link(l)
        if not data:
            link = extract_final_links(True,l)
            data = [{"stream_url":link}]
        return data
        
    
    else:    #for adult animes
        data =  decode_from_base64(l)
        if not data:
            print(red("[*]Seems like link is not available"))
            exit()
        return data
            
        
    
    
        
