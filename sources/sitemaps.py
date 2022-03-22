# %%

def sitemaps_from_robots_txt(url):
    import requests
    import urllib.parse
    parts = urllib.parse.urlparse(url)
    urlrobots = parts.scheme + '://' + parts.netloc + '/robots.txt'
    r = requests.get(urlrobots)
    text = r.text.lower() if r.status_code == 200 else None
    sitemaps_lines = list(filter(lambda l:l.startswith('sitemap:'), text.split('\n')))
    sitemaps = [(s.split('sitemap:')[1]).strip() for s in sitemaps_lines]
    #remove gz

# %%

def sitemap_content(url):
    from gzip import decompress, BadGzipFile
    import requests
    def content_gz(url):
        try:
            return decompress(requests.get(url).content)
        except BadGzipFile :
            return requests.get(url).text
    return content_gz(url) if url.endswith('.gz')\
        else requests.get(url).text


# %%
#def sitemap_type(sitemap_content):
#    return 'gnews' if 'schemas/sitemap-news' in sitemap_content else\
