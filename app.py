#trying out new shit
from __future__ import print_function, unicode_literals
from codebase.gogoplay import *
from codebase.allanime import *
from codebase.search import *
import os
import regex
from PyInquirer import style_from_dict, Token, prompt, Separator
from colorama import Fore, Style


#soem global shit
dub_prefix = False
player = "mpv"
lmagenta = lambda a: f"{Fore.LIGHTMAGENTA_EX}{a}{Style.RESET_ALL}"

#provider list
PROVIDER_LIST = (
    ("gogoplay", regex.compile("(streaming|load)\.php\?")),
    ("doodstream", "https://dood.to/"),
    ("okru", "https://ok.ru"),
    ("streamlare", "https://streamlare.com"),
    ("mp4upload", "https://mp4upload.com/")
)

'''
start of UI
'''
#style shit
style = style_from_dict({
    Token.Separator: '#cc5454',
    Token.QuestionMark: '#673ab7 bold',
    Token.Selected: '#cc5454',  # default
    Token.Pointer: '#673ab7 bold',
    Token.Instruction: '',  # default
    Token.Answer: '#f44336 bold',
    Token.Question: '#673ab7 bold',
})

questions = [
    {
        'type': 'list',
        'message': 'Choose provider',
        'name': 'provider',
        'choices': [
            Separator('= The Providers ='),
            {
                'name' : 'gogoplay'
            },
            {
                'name' : 'allanime'
            }
        ]
        
        
        
    }
]

answers = prompt(questions,style=style)

provider = answers["provider"]
'''
end of UI
'''
def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def ask_al_provider(links):
    """_summary_

    Args:
        links (list): create a list of links with available extractors
    """
    final_links = []
    final_names = []
    for i in links:
        for name, site_url in PROVIDER_LIST:
            if isinstance(site_url, regex.Pattern):
                if site_url.search(i):
                    final_links.append(i)
                    final_names.append(name)
                continue

            if site_url in i:
                final_links.append(i)
                final_names.append(name)
    #create Ui
    provider_questions = [
        {
            'type':"list",
            'message' : 'Choose provider',
            'name' : 'provider',
            'choices' : final_names
        }
    ]
    answers = prompt(provider_questions,style=style)
    name =  answers["provider"]
    return final_links[final_names.index(name)]                
    


clear()
query = input(lmagenta("Enter the anime name: "))
x = search(query)

anime_question=[
    {
        'type':'list',
        'message':'Choose the anime',
        'name':'anime',
        'choices':x
    }
]
answers = prompt(anime_question,style=style)
anime_to_watch = answers["anime"]

if provider == "gogoplay":
    from_al = False

    data = extract_episode_info(anime_to_watch)
    p = input(lmagenta(f"[*]Enter episode(total {data['eptotal']}): "))
    link = "https:" + data[str(int(p)-1)]
    qualities , links = extract_final_links(from_al,link)
    clear()
    quality_question = [
        {
            'type' : 'list',
            'message': 'Choose qulaity',
            'name': 'quality',
            'choices': qualities
        }
    ]
    answers = prompt(quality_question,style=style)
    quality = answers["quality"]

    final_link = links[qualities.index(quality)]
    #print(final_link)
    os.system(f'{player} --referrer="https://gogoplay.io" {final_link}')

else:
    if "-dub" in anime_to_watch:
        dub_prefix = True
    data = al_extract_episode_info(dub_prefix,anime_to_watch)
    p = input(lmagenta(f"[*]Enter episode(total {data['eptotal']}): "))
    links = data[str(int(p)-1)]
    #print(links)
    x = ask_al_provider(links)
    
    referrer,link = al_return_link(x)
    
    os.system(f'{player} --referrer="{referrer}" "{link}"' if len(referrer)>0 else f'{player} "{link}"')
