#!/usr/bin/env python
import feedparser, urllib.parse, urllib, logging, requests
from logging import debug, info, warning, error
import requests, concurrent.futures

def retrieve_rss(rss):
    """
    Request of the rss file 
    """
    response = requests.get(url=rss, timeout=5, allow_redirects=True)
    feed = feedparser.parse(response.content)
    info(f"retrieve rss: {rss}")
    for post in feed.entries:
        debug( post.title)
        debug(post.link)
    return feed

def get_youtube_rss(inpu):
    """
    Get the rss url from a youtube channel
    """
    if '/channel/' in inpu:
        return "https://www.youtube.com/feeds/videos.xml?channel_id="+ inpu.split("/channel/")[1].split('/')[0].split('?')[0]
    if '/user/' in inpu:
        return "https://www.youtube.com/feeds/videos.xml?user=" + inpu.split("/user/")[1].split('/')[0].split('?')[0]

def retrieve_input(inpu):
    """
    Retrieve the input. Can be a youtube channel url, a rss url, or a google news input formated as : "googlenews-fr-fr: blablabla"
    """
    print('input', inpu)
    if inpu.startswith('https://youtube.com/') or inpu.startswith('https://www.youtube.com/'):
        info('YOUTUBE')
        rss = get_youtube_rss(inpu)
        return retrieve_rss(rss)
    if inpu.startswith('googlenews'):
        (country,search) = inpu.split(':')
        (tmp, lang, country) = ('', 'en', 'en') if country=='googlenews' else country.split('-')
        params = {'hl':lang, 'gl':country, 'ceid':country+':'+lang, 'q':search.strip()}
        urllib.parse.urlencode(params)
        request = f'https://news.google.com/rss/search?' + urllib.parse.urlencode(params)  #hl={lang}&gl={country}&ceid={country}:{lang}&search?q={search_prep}'
        info(f'google news {lang}, {country}, {request}')
        return retrieve_rss(request)
    retrieve_rss(inpu)

def retrieve_inputs(inputs):
    """
    Multithreaded version of retrieve_input
    """
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = []
        for inp in inputs:
            futures.append(executor.submit(retrieve_input, inp))
        results = []
        for future in concurrent.futures.as_completed(futures):
            try:
                results.append(future.result())
            except requests.ConnectTimeout:
                info("ConnectTimeout.")      
        return results     



#---------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------
if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    #retrieve_input("googlenews-fr-fr: paleoanthropologie")
    #print()
    #retrieve_input("https://www.youtube.com/channel/UC3E2DhYIqnoc6H3WXwTVnlA")
    #print() 
    #retrieve_input("http://radiofrance-podcast.net/podcast09/rss_14312.xml") 

    print("-----------------------") 
    retrieve_inputs(["googlenews-fr-fr: paleoanthropologie", \
        "https://www.youtube.com/channel/UC3E2DhYIqnoc6H3WXwTVnlA",\
            "http://radiofrance-podcast.net/podcast09/rss_14312.xml"]) 