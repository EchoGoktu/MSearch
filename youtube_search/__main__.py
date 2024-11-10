from youtube_search import YoutubeSearch
from pprint import pprint
from sys import argv

def get_argv(index, default=None) :
    try :
        return argv[index]
    except :
        return default    

if get_argv(1) is not None and get_argv(2) is not None :
    results = YoutubeSearch(get_argv(1), max_results=int(get_argv(2))).to_dict()
    pprint(results)

else :
    print("Invalid Input")

