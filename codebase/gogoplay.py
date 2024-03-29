from .httpclient import HttpClient
from bs4 import BeautifulSoup as bs
from Cryptodome.Cipher import AES
import re
import base64
import json
import yarl
from .m3u8 import *
import httpx

req = HttpClient()


#some global shit
base_url = "https://animixplay.to"
s=b'37911490979715163134003223491201'
s_2 = b'54674138327930866480207815084989'
iv= b'3134003223491201'



def extract_episode_info(anime_id):
    r=req.get(
        f"{base_url}{anime_id}"
    )
    soup = bs(r.text,"html.parser")
    data = json.loads(soup.select("#epslistplace")[0].text)
    return data
    
#some helper function
def get_crypto(url):
    '''
    function to get crypto data
    '''
    r=req.get(url)
    soup = bs(r.content,'lxml')
    for item in soup.find_all('script',attrs={'data-name':'episode','data-value':True}):
        crypto = str(item['data-value'])
    return crypto    

def pad(data):
    '''
    helper function
    '''
    return data + chr(len(data) % 16) * (16 - len(data) % 16)


def decrypt(key,data):
    '''
    function to decrypt data
    '''
    return AES.new(key, AES.MODE_CBC, iv=iv).decrypt(base64.b64decode(data))


def extract_final_links(from_al,link):
    
    
    crypto_data=get_crypto(link)
    # #get the decrypted crypto value
    decrypted_crypto = decrypt(s,crypto_data)
    new_id = decrypted_crypto[decrypted_crypto.index(b"&"):].strip(b"\x00\x01\x02\x03\x04\x05\x06\x07\x08\t\n\x0b\x0c\r\x0e\x0f\x10").decode()
    
    
    p_url = yarl.URL(link)
    
    ajax_url = "https://{}/encrypt-ajax.php".format(p_url.host)

    encrypted_ajax = base64.b64encode(
        AES.new(s,AES.MODE_CBC,iv=iv).encrypt(
            pad(p_url.query.get('id')).encode()
        )
    )

    #send the request (httpx bug not working)
    r =httpx.get(
        f'{ajax_url}?id={encrypted_ajax.decode()}{new_id}&alias={p_url.query.get("id")}',
        
        headers={'x-requested-with': 'XMLHttpRequest'}
    )
    

    j = json.loads(
        decrypt(s_2,r.json().get("data")).strip(
            b"\x00\x01\x02\x03\x04\x05\x06\x07\x08\t\n\x0b\x0c\r\x0e\x0f\x10"
        )
    )
    #print(j)
    if from_al:
        return  j['source'][0]['file']
    else:
        audio,qualities,links = get_m3u8_quality(j['source'][0]['file'])
        
    
        return audio,qualities,links