from .httpclient import HttpClient
import json 
import re


req = HttpClient()

#search shit 
search_url = "https://v1.w0ltfgqz8y3ygjozgs4v.workers.dev"
anime_pattern = r'<a href="\/v1\/(.*?)"'

def search(query):
    r=req.post(
        search_url,
        data={
        "q2" : query.replace(" ","+"),
        }
    )

    data = json.loads(r.text)
    
    #collect and return anime ids
    x = re.findall(anime_pattern,str(data))
    
    return list(set(x)) #delete duplicates and return
    

