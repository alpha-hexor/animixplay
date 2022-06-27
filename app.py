from codebase.ui import *
from codebase.gogoplay import *
from codebase.animix import *
from codebase.search import *
from codebase.stream import *

#some global shit
provider = ask_provider()
clear()
query = input(lmagenta("[*]Enter the anime name: "))
animes = search(query)
x = [i.replace("/v1/","") for i in animes]

anime_name = ask_anime_name(x)
anime_to_watch = animes[x.index(anime_name)]




if provider == "gogoplay":
    from_al = False

    data = extract_episode_info(anime_to_watch)
    p = input(lmagenta(f"[*]Enter episode(total {data['eptotal']}): "))
    link = "https:" + data[str(int(p)-1)]
    try:
        audio,qualities , links = extract_final_links(from_al,link)
        

        quality = ask_quality(qualities)
        final_link = links[qualities.index(quality)]
        play_mpv([{"stream_url":final_link,"audio":audio,"referrer":"https://goload.pro","name":f"{anime_name}_{p}"}])

    except:
        print(red("[*]Change provider"))

else:
    data = extract_episode_info(anime_to_watch)
    
    p = input(lmagenta(f"[*]Enter episode(total {data['eptotal']}): "))
    
    links = data[str(int(p)-1)]
    
    streaming_data = generate_link(links)[0]
    
    streaming_data["name"] = f"{anime_name}_{p}"
    
    play_mpv([streaming_data])
    
    