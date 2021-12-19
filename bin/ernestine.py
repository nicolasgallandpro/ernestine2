#!/usr/bin/env python
import argparse, os, yaml, feedparser, urllib.parse, urllib

parser = argparse.ArgumentParser()
parser.add_argument("--rsnl", help="Newsletter")
parser.add_argument("--rsc", help="Flux rsc")
parser.add_argument("--rss", help="Flux rss")
parser.add_argument("--input", help="Flux rss or youtube or google news")
args = parser.parse_args()

print(args.rsnl, args.rsc, args.rss)

def get_youtube_rss(inpu):
    if '/channel/' in inpu:
        return "https://www.youtube.com/feeds/videos.xml?channel_id="+ inpu.split("/channel/")[1].split('/')[0].split('?')[0]
    if '/user/' in inpu:
        return "https://www.youtube.com/feeds/videos.xml?user=" + inpu.split("/user/")[1].split('/')[0].split('?')[0]

def retrieve_input(inpu):
    print('input', inpu)
    if 'rsc' in inpu:
        raise Exception('not yet implemented')
    if inpu.startswith('https://youtube.com/') or inpu.startswith('https://www.youtube.com/'):
        print('YOUTUBE')
        rss = get_youtube_rss(inpu)
        retrieve_rss(rss)
        return
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
    feed = feedparser.parse(rss)

    print()
    for post in feed.entries:
        print('----', post.title)
        print(post.link)


def parse_rsc_file(rsc_file):
    content = urllib.request.urlopen(rsc_file).read() if rsc_file.startswith('http') else open(rsc_file).read()
    rsc = yaml.load( content, yaml.SafeLoader)
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
if args.rsc != None:
    print(parse_rsc_file(args.rsc))
