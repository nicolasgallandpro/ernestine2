#!/usr/bin/env python
import feedparser, urllib.parse, urllib, logging, json, datetime
import yaml
from logging import debug, info, warning, error
from pprint import pprint
from inputs import retrieve_input, retrieve_inputs
from datetime import date
import dateutil.parser
import copy

KEYWORDS = {
    'keep_filter':'keep_only', 
    'limit_posts':'limit_posts',
    'max_age':'max_age_minutes'
}

class Parsed_rsc:
    name = None
    categories = None
    description = None
    max_age_minutes = None

    class Category:
        name = None
        feeds = None
        import_feeds_from = None # file:category  Example:  example.rsc:science
        keep_only = None  #python like
        def __init__(self, name, import_feeds_from=None, keep_only=None):
            self.name, self.import_feeds_from, self.keep_only = name, import_feeds_from, keep_only
        def __str__(self):
            print('-', self.name, self.import_feeds_from, self.keep_only)
            return str([str(feed) for feed in self.feeds])

    class Feed:
        name = None
        inpuut = None
        keep_only = None
        def __init__(self, name, inpuut, keep_only=None):
            self.name, self.inpuut, self.keep_only = name, inpuut, keep_only
        def __str__(self):
            print('-','-',self.name, self.inpuut, self.keep_only)
            return ''

        #------------------------------------        
    def __str__(self):
        print(self.name, self.description, self.max_age_minutes)
        return str([str(c) for c in self.categories])
    
    def __init__(self, rsc_file, recur=0):
        if recur>100:
            raise Exception('Infinite loop ? more than 100 recursive rsc parse')
        content = urllib.request.urlopen(rsc_file).read() if rsc_file.startswith('http') else open(rsc_file).read()
        rsc = yaml.load( content, yaml.SafeLoader)
        self.name, self.description, self.max_age_minutes = rsc['name'], rsc.get('description'), rsc.get('max_age_minutes')
        self.categories = [] 
        for category in rsc['categories']:
            parsed_category = self.Category(category.get('name'), category.get('import_feeds_from'), category.get('keep_only'))
            parsed_category.feeds = self.get_feeds_of_category(category) 
            self.categories.append(parsed_category)

    def get_feeds_of_category(self, category_conf):
        if 'import_feeds_from' in category_conf:
            origin = category_conf['import_feeds_from']
            imported_rsc = Parsed_rsc(origin.split(':')[0] if ':' in origin else origin)
            imported_category_name = origin.split(':')[1] if ':' in origin else category_conf['name']
            print(imported_category_name)
            imported_category = (list(filter(lambda c:c.name==imported_category_name, imported_rsc.categories)))[0] 
            #todo erreur propre si le nom de catégory n'existe pas 
            return imported_category.feeds
        feeds = []
        for i, feed in enumerate(category_conf['feeds']):
            possibles_names = []
            for entry_key in feed.keys():
                if entry_key not in KEYWORDS.values():
                    possibles_names.append(entry_key)
            if len(possibles_names) == 0:
                raise Exception(f'The input number {i} has no name')
            if len(possibles_names)>1:
                raise Exception(f'Category: {category_conf["name"]} : The input number {i} has {len(possibles_names)} possible names : {",".join(possibles_names)}')
            feed_name = possibles_names[0]
            parsed_feed = self.Feed(feed_name, feed[feed_name], feed.get('keep_only'))
            feeds.append(parsed_feed)
        return feeds 
   


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
    #inputs = []
    #for category in rsc_conf['categories']:
    #    inputs += [ feed['inpuut'] for feed in category['feeds']]
    #raw = retrieve_inputs(inputs)
    #return raw
    inputs = []
    for category in rsc_conf.categories:
        inputs += [ feed.inpuut for feed in category.feeds]
    raw = retrieve_inputs(inputs)
    return raw


def format_entry(entry, feed):
    """
    Helper : Create an object with unified informations (title, source, ...) for all types of feeds (atom, rss, youtube, google news, podcasts ...)
    """
    link = entry['link'] 
    url = link if type(link)==type('') else link['href']  
    in_entry = lambda e:e if e in entry.keys() else False
    published_key = in_entry('pubDate') or in_entry('published') or None
    if entry.get(published_key) == None :
        info(f"!!! une entrée de {feed.name} n'a pas de publish date")
    return {
        'source': entry['source']['title'] if 'source' in entry else feed.name if type(link)==type('') else link['name'], 
        'url': url,
        'title': entry['title'],
        'summary': entry.get('summary') or '',
        'id': entry.get('id'),
        'published': entry.get(published_key),
        'author': entry['author'] if 'author' in entry else None,
        'image': entry['media_content'] if 'media_content' in entry and \
            ('jpg' in entry['media_content'] or 'jpeg' in entry['media_content']) else None
    }
def entry_keep_filter(keep_filter, formated_entry):
    """
    Helper : eval keep filter. 
    Args : feed, formated entry
    """
    f = formated_entry
    prep = lambda t:t.lower() if t!=None else None
    source, url, title, summary, text, author = (prep(f['source']), prep(f['url']), prep(f['title']), \
                    prep(f['summary']), prep(f['title'] + ' '+ f['summary']), prep(f['author']))
    return eval(keep_filter.lower()) 
    #if KEYWORDS['keep_filter'] not in feed :
    #    debug('no filter')
    #    return True;
    #if eval((feed[KEYWORDS['keep_filter']]).lower()):
    #    debug('filter OK')
    #    return True
    #else:
    #    debug('filter KO !!')
    #    return False

def max_age_filter(rsc_conf, entry):
    """
    Helper : eval max age filter
    """
    if rsc_conf.max_age_minutes == None : 
        return True
    if 'published' not in entry:
        debug('published not in entry, so entry is filtered')
        return False 
    age_s = (datetime.datetime.utcnow().replace(tzinfo=None) - dateutil.parser.parse(entry['published']).replace(tzinfo=None)).total_seconds()
    debug(f'time filter. keep ? {(age_s/60) < rsc_conf.max_age_minutes} age minutes : {age_s/60} max {rsc_conf.max_age_minutes}')
    return (age_s/60) < rsc_conf.max_age_minutes

#-------------------- interprete rsc
def prepare_curation_data_without_thumbnails(rsc_conf, raw_results):
    """
    Makes a well formated object with categories, sources, ordered posts
    """
    #if pas google news : ajouter la source 
    rsc_conf.last_update = datetime.datetime.now().strftime("%d/%m/%y %H:%M") 
    for category in rsc_conf.categories:
        category.entries = []
        for feed in category.feeds:
            if feed.inpuut not in raw_results:
                info(f"le feed {feed.name} n'a pas donné de réponse")
                continue
            data = raw_results[feed.inpuut]
            for entry in data.entries:
                try:
                    formated_entry = format_entry(entry, feed)
                    debug(entry['title'])
                    #applying filters
                    feed_keep_filter_passed = True if feed.keep_only == None else entry_keep_filter(feed.keep_only, formated_entry)
                    category_keep_filter_passed = True if category.keep_only == None else entry_keep_filter(category.keep_only, formated_entry)
                    if feed_keep_filter_passed and category_keep_filter_passed and max_age_filter(rsc_conf, entry): 
                        category.entries.append(formated_entry)
                except:
                    info(f'error with the an entry of {feed.name}')
                    continue
        #newer first:
        (category.entries).sort(key=lambda x: dateutil.parser.parse(x['published']), reverse=True)
                
    return rsc_conf


def print_formated_posts(formated_posts):
    """
    """
    for category in formated_posts.categories:
        print('---------------', category.name)
        for post in category.entries:
            print(post['published'], post['source'], '---', post['title'])
            print(post['url'])


#---------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    p = Parsed_rsc("/Users/nicolas/Documents/dev/ernestine/ernestine2/input/fact_checking.rsc")
    str(p)
    raw = get_raw_posts(p)
    #rsc_conf = parse_rsc_file("/Users/nicolas/Documents/dev/ernestine/ernestine2/input/medias_indeps.rsc")
    #pprint(rsc_conf)

    #raw = get_raw_posts(rsc_conf)
    #print(raw.keys())

    formated_posts = prepare_curation_data_without_thumbnails(p, raw) 
    print_formated_posts(formated_posts) 
    