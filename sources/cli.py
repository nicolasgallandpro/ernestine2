#!/usr/bin/env python
import argparse, urllib, yaml, feedparser, logging
from logging import debug, info, warning, error
from inputs import retrieve_input

logging.basicConfig(level=logging.DEBUG)

parser = argparse.ArgumentParser()
parser.add_argument("--rsnl", help="Newsletter")
parser.add_argument("--rsc", help="Flux rsc")
parser.add_argument("--rss", help="Flux rss")
parser.add_argument("--input", help="Flux rss or youtube or google news")
args = parser.parse_args()

print(args.rsnl, args.rsc, args.rss)


#---------------------------------------
if args.rsnl == None and args.rsc == None and args.rss == None and args.input == None:
    files = [f for f in os.listdir('.') if os.path.isfile(f)]
    print('------------------------------')
    print('---------- newsletters -------')
    print('------------------------------')
    print()
    for f in files:
        print(f) if '.rsnl' in f else None
    print()
    print()
    print('------------------------------')
    print('---------- flux --------------')
    print('------------------------------')
    for f in files: 
        print()
        if '.rsc' in f:
            print('------', f) 
            rsc = parse_rsc_file(f)
            print('name:', rsc['name'])
            print('description:', rsc['description'])
            for inp in rsc['input']:
                print('-', inp)
    print()

#-----------------------------------
if args.rss != None:
    retrieve_rss(args.rss)
if args.input != None:
    print('---------input', args.input)
    retrieve_input(args.input)
if args.rsc != None:
    print(parse_rsc_file(args.rsc))



