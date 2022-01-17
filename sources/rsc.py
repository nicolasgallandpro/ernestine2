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
    for i, inp in enumerate(rsc['feeds']):
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
            
    return rsc







#---------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------
if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    from pprint import pprint
    pprint(parse_rsc_file("/Users/nicolas/Documents/dev/ernestine/ernestine2/input/example.rsc"))

    