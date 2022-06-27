#code for user interface
from __future__ import print_function, unicode_literals
from PyInquirer import style_from_dict, Token, prompt, Separator
import os
from colorama import Fore, Style

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

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

#ui to ask provider
def ask_provider():
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
                    'name' : 'animixplay'
                }
            ]
            
            
            
        }
    ]

    answers = prompt(questions,style=style)

    return answers["provider"]

#ui to ask anime name
def ask_anime_name(x):
    anime_question=[
        {
            'type':'list',
            'message':'Choose the anime',
            'name':'anime',
            'choices':x
        }
    ]
    answers = prompt(anime_question,style=style)
    return answers["anime"]

#ui to ask quality
def ask_quality(qualities):
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
    return answers["quality"]

#color print
lmagenta = lambda a: f"{Fore.LIGHTMAGENTA_EX}{a}{Style.RESET_ALL}"
red = lambda a: f"{Fore.RED}{a}{Style.RESET_ALL}"