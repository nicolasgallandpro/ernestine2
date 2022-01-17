#!/usr/bin/env python
import feedparser, urllib.parse, urllib, logging
import yaml
from logging import debug, info, warning, error
from inputs import retrieve_input, retrieve_inputs



def parse_rsc_file(rsc_file):
    content = urllib.request.urlopen(rsc_file).read() if rsc_file.startswith('http') else open(rsc_file).read()
    rsc = yaml.load( content, yaml.SafeLoader)
    return rsc







#---------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------
if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    from pprint import pprint
    pprint(parse_rsc_file("/Users/nicolas/Documents/dev/ernestine/ernestine2/input/example.rsc"))

    