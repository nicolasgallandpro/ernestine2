#!/usr/bin/env python
import argparse, os, yaml, feedparser, urllib.parse

parser = argparse.ArgumentParser()
parser.add_argument("--rsnl", help="Newsletter")
parser.add_argument("--rsc", help="Flux rsc")
parser.add_argument("--rss", help="Flux rss")
parser.add_argument("--input", help="Flux rss or youtube or google news")
args = parser.parse_args()

print(args.rsnl, args.rsc, args.rss)

def retrieve_input(inpu):
    if 'rsc' in inpu:
        raise Exception('not yet implemented')
    if inpu.startswith('https://youtube.com/'):
        raise Exception('not yet implemented')
    if inpu.startswith('googlenews'):
        (country,search) = inpu.split(':')
        (tmp, lang, country) = country.split('-')
        params = {'hl':lang, 'gl':country, 'ceid':country+':'+lang, 'q':search.strip()}
        urllib.parse.urlencode(params)
        request = f'https://news.google.com/rss/search?' + urllib.parse.urlencode(params)  #hl={lang}&gl={country}&ceid={country}:{lang}&search?q={search_prep}'
        print('google news', lang, country, request)
        retrieve_rss(request)
        return
    retrieve_rss(inpu)

def retrieve_rss(rss):
    #feed = feedparser.parse('https://news.google.com/rss/search?q=neolithic')
    feed = feedparser.parse(rss)
    # https://news.google.com/rss?hl=<LANGUAGE_CODE>&gl=<COUNTRY_CODE>&ceid=<COUNTRY_CODE>:<LANGUAGE_CODE>

    print()
    for post in feed.entries:
        print(post.title)


def parse_rsc_file(rsc_file):
    if rsc_file.startswith('http'):
        raise Exception('not yet implemented')
    rsc = yaml.load(open(rsc_file).read(), yaml.SafeLoader)
    return rsc


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
