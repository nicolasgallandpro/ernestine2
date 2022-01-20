#!/usr/bin/env python
import feedparser, urllib.parse, urllib, logging, requests
from logging import debug, info, warning, error
import requests, concurrent.futures, redis as _redis

redis = _redis.Redis()

def retrieve_rss(rss):
    """
    Request of the rss file for cache (redis) or from the web
    """
    
    # case cache
    if redis.exists(rss):
        info('%% from cache: '+rss)
        return feedparser.parse(redis.get(rss))
    
    # case request
    response = requests.get(url=rss, timeout=45, allow_redirects=True)
    feed = feedparser.parse(response.content)
    info(f"retrieve rss: {rss}")
    for post in feed.entries:
        debug( post.title)
        debug(post.link)
    redis.set(rss, response.content, ex=600)
    return feed

def get_youtube_rss(inpu):
    """
    Get the rss url from a youtube channel
    """
    if '/channel/' in inpu:
        return "https://www.youtube.com/feeds/videos.xml?channel_id="+ inpu.split("/channel/")[1].split('/')[0].split('?')[0]
    if '/user/' in inpu:
        return "https://www.youtube.com/feeds/videos.xml?user=" + inpu.split("/user/")[1].split('/')[0].split('?')[0]

def retrieve_input(inpu, add_keys=False):
    """
    Retrieve the input. Can be a youtube channel url, a rss url, or a google news input formated as : "googlenews-fr-fr: blablabla"
    """
    original_inpu = inpu
    print('input', inpu)
    if inpu.startswith('https://youtube.com/') or inpu.startswith('https://www.youtube.com/'):
        info('YOUTUBE')
        inpu = get_youtube_rss(inpu)
    if inpu.startswith('googlenews'):
        (country,search) = inpu.split(':')
        (tmp, lang, country) = ('', 'en', 'en') if country=='googlenews' else country.split('-')
        params = {'hl':lang, 'gl':country, 'ceid':country+':'+lang, 'q':search.strip()}
        urllib.parse.urlencode(params)
        inpu = f'https://news.google.com/rss/search?' + urllib.parse.urlencode(params)  #hl={lang}&gl={country}&ceid={country}:{lang}&search?q={search_prep}'
        info(f'google news {lang}, {country}, {inpu}')
    return (original_inpu,retrieve_rss(inpu)) if add_keys else retrieve_rss(inpu)  

def retrieve_inputs(inputs):
    """
    Multithreaded version of retrieve_input
    """
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = []
        for inp in inputs:
            futures.append(executor.submit(retrieve_input, inp, True))
        results = {}
        for future in concurrent.futures.as_completed(futures):
            try:
                inpu, res = future.result()
                results[inpu] = res
            except requests.ConnectTimeout:
                info("ConnectTimeout.")      
        return results     



#---------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------
if __name__ == "__main__":
    from pprint import pprint
    logging.basicConfig(level=logging.INFO)
    #retrieve_input("googlenews-fr-fr: paleoanthropologie")
    #print()
    #retrieve_input("https://www.youtube.com/channel/UC3E2DhYIqnoc6H3WXwTVnlA")
    #print() 
    #retrieve_input("http://radiofrance-podcast.net/podcast09/rss_14312.xml") 
    #pprint(out)
    print("-----------------------") 
    ins = ["googlenews-fr-fr: paleoanthropologie", \
        "https://www.youtube.com/channel/UC3E2DhYIqnoc6H3WXwTVnlA",\
            "http://radiofrance-podcast.net/podcast09/rss_14312.xml",\
             "https://www.lemonde.fr/pixels/rss_full.xml",\
             "https://rss.nytimes.com/services/xml/rss/nyt/Science.xml"       ]
    outs = retrieve_inputs(ins) 

    for k in outs.keys():
        print('----------', k)
        o = outs[k]
        if o:
            pprint(o.entries[0].keys())
            if 'source' in o.entries[0]:
                print('source', o.entries[0].source)
            if 'author' in o.entries[0]:
                print('author', o.entries[0].author)
            if 'published' in o.entries[0]:
                print('pusblished', o.entries[0].published)
        else:
            print('?')
    