#!/usr/bin/env python
import feedparser, urllib.parse, urllib, logging
import yaml
from logging import debug, info, warning, error
from pprint import pprint
from inputs import retrieve_input, retrieve_inputs

KEYWORDS = ['keep_only', 'limit_posts']

def parse_rsc_file(rsc_file):
    """
    - retrieve rsc file in local disk or on the web
    - check rsc format
    - add 'inpuut' and 'name' entries to each feed entry
    """
    content = urllib.request.urlopen(rsc_file).read() if rsc_file.startswith('http') else open(rsc_file).read()
    rsc = yaml.load( content, yaml.SafeLoader)
    pprint(rsc)

    # name
    if 'name' not in rsc:
        raise Exception("The rsc file as no 'name' entry")
    for category in rsc['categories']:
        for i, inp in enumerate(category['feeds']):
            possibles_names = []
            for entry_key in inp.keys():
                if entry_key not in KEYWORDS:
                    possibles_names.append(entry_key)
            if len(possibles_names) == 0:
                raise Exception(f'The input number {i} has no name')
            if len(possibles_names)>1:
                raise Exception(f'The input number {i} has {len(possibles_names)} possible names : {",".join(possibles_names)}')
            inp['inpuut'] = inp[possibles_names[0]]
            inp['name'] = possibles_names[0]
            del inp[possibles_names[0]]
            
    return rsc


def get_raw_posts(rsc_conf):
    """
    Retrieve not filtered posts for a rsc conf. 
    Args : Expected format for rsc_conf : [
        'name':'...', ..., 
        categories:[
            name: "categoryX",
            'feeds':[{
                name:'...',
                inpuut:'htpps://.....'
            }, ...]
    ] 
    Output : dictionnary whose keys are inpuuts (rss urls, youtube channel, ....) and values are rss data :
        {'inpuutxxxx': __rss_data__ }
    """
    inputs = []
    for category in rsc_conf['categories']:
        inputs += [ feed['inpuut'] for feed in category['feeds']]
    raw = retrieve_inputs(inputs)
    return raw

def prepare_curation_data_without_thumbnails(rsc_conf, raw_results, time_filtered=False):
    """
    Makes a well formated object with categories, sources, ordered posts
    """
    if time_filtered:
        raise NotImplementedError()
    #if pas google news : ajouter la source 
    print()


def print_formated_posts(formated_posts):
    """
    """
    for category in formated_posts.categories:
        print('---------------', category.name)
        for post in category.posts:
            print(post.published, post.title)
            print(post.url)


#---------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    from pprint import pprint
    
    rsc_conf = parse_rsc_file("/Users/nicolas/Documents/dev/ernestine/ernestine2/input/example.rsc")
    pprint(rsc_conf)

    raw = get_raw_posts(rsc_conf)
    print(raw.keys())

    formated_posts = prepare_curation_data_without_thumbnails(rsc_conf, raw_results, time_filtered=False) 
    print_formated_posts(formated_posts) 
    