#!/usr/bin/env python
import feedparser, urllib.parse, urllib, logging, requests
from logging import debug, info, warning, error
import requests, concurrent.futures, redis as _redis
from typing import List, Tuple, Dict
import dateutil.parser, datetime


"""
Helpers that retrieve raw inputs of rss/sitemaps
"""


redis = _redis.Redis()

def retrieve_rss(rss):
    """
    Request of the rss file for cache (redis) or from the web
    """
    
    # case cache
    if redis.exists(rss):
        debug('%% from cache: '+rss)
        return feedparser.parse(redis.get(rss))
    
    # case request
    response = requests.get(url=rss, timeout=5, allow_redirects=True)
    feed = feedparser.parse(response.content)
    debug(f"retrieve rss: {rss}")
    for post in feed.entries:
        debug( post.title)
        debug(post.link)
    redis.set(rss, response.content, ex=600) # cache de 10 minutes du résultat de la requete
    return feed

def get_youtube_rss(inpu: str):
    """
    Get the rss url from a youtube channel
    """
    if '/channel/' in inpu:
        return "https://www.youtube.com/feeds/videos.xml?channel_id="+ inpu.split("/channel/")[1].split('/')[0].split('?')[0]
    if '/user/' in inpu:
        return "https://www.youtube.com/feeds/videos.xml?user=" + inpu.split("/user/")[1].split('/')[0].split('?')[0]
    if '.xml' in inpu:
        return inpu
    if 'playlist?list=' in inpu:
        return 'https://www.youtube.com/feeds/videos.xml?playlist_id=' + inpu.split('list=')[1]

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
    res = retrieve_rss(inpu)
    return (original_inpu,res) if add_keys else res  

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
            except :
                error('!!!!!!!!!!!!! erreur sur ')
        return results     



class Entry:
    """
    A post entry of rss or sitemap
    """
    source: str; url: str; title: str; summary: str = None; id: str = None; 
    published:str = None; published_key: str = None; author: str= None; image: str = None
    def __init__(self, raw_entry: Dict, feed_name: str):
        """
        Helper : Create an object with unified informations (title, source, ...) for all types of feeds (atom, rss, youtube, google news, podcasts ...)
        """
        link = raw_entry['link'] 
        in_entry = lambda e:e if e in raw_entry.keys() else False
        published_key = in_entry('pubDate') or in_entry('published') or in_entry('updated') or None
        if raw_entry.get(published_key) == None :
            info(f"!!! une entrée de {feed_name} n'a pas de publish date. {str(','.join(raw_entry.keys()))}")
        
        self.source = raw_entry['source']['title'] if 'source' in raw_entry else feed_name if type(link)==str else link['name']
        self.url = link if type(link)==str else link['href']  
        self.title = raw_entry['title']
        self.summary = raw_entry.get('summary') or ''
        self.id = raw_entry.get('id')
        self.published = raw_entry.get(published_key)
        self.published_key = published_key
        self.author = raw_entry['author'] if 'author' in raw_entry else None
        self.image = raw_entry['media_content'] if 'media_content' in raw_entry and \
            ('jpg' in raw_entry['media_content'] or 'jpeg' in raw_entry['media_content']) else None


    def keep_filter(self, keep_filter: str) -> bool:
        """
        Helper : eval keep filter. 
        Args : feed, formated entry
        """
        prep = lambda t:t.lower() if t!=None else None
        source, url, title, summary, text, author = (prep(self.source), prep(self.url), prep(self.title), \
                        prep(self.summary), prep(self.title + ' '+ self.summary), prep(self.author))
        return eval(keep_filter.lower()) 


    def max_age_filter(self, max_age_minutes: int) -> bool:
        """
        Helper : eval max age filter
        """
        
        if self.published == None:
            debug('published not in entry, so entry is filtered')
            return False 
        age_s = (datetime.datetime.utcnow().replace(tzinfo=None) - dateutil.parser.parse(self.published).replace(tzinfo=None)).total_seconds()
        debug(f'time filter. keep ? {(age_s/60) < max_age_minutes} age minutes : {age_s/60} max {max_age_minutes}')
        return (age_s/60) < max_age_minutes




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
    