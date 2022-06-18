from .httpclient import HttpClient
import re


req = HttpClient()

#search shit 
search_url = "https://cachecow.eu/api/search"
anime_pattern = r'<a href="(.*?)"'
title_patter = r'title="(.*?)"'


def search(query):
    r=req.post(
        search_url,
        data={
        "qfast" : query,
        }
    ).json().get("result")

    #animes
    anime_ids = re.findall(anime_pattern,r)
    return list(set(anime_ids)) #delete duplicates and return
    

