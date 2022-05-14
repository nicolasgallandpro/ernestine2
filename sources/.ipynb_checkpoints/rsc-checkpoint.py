#!/usr/bin/env python
import feedparser, urllib.parse, urllib, logging, json, datetime
from typing import List, Tuple, Dict
import yaml
from logging import debug, info, warning, error
from pprint import pprint
from entries import retrieve_input, retrieve_inputs, Entry
from datetime import date
import dateutil.parser
import copy

KEYWORDS = {
    'keep_filter':'keep_only', 
    'limit_posts':'limit_posts',
    'max_age':'max_age_minutes'
}


class Feed:
    name: str = None
    inpuut: str = None
    keep_only:str = None
    def __init__(self, name: str, inpuut: str, keep_only=None):
        self.name, self.inpuut, self.keep_only = name, inpuut, keep_only
    def __str__(self):
        #print('-','-',self.name, self.inpuut, self.keep_only)
        return ''

    
class Category:
    name: str = None
    feeds: List[Feed] = None
    import_feeds_from: str = None # file:category  Example:  example.rsc:science
    keep_only:str = None  #python like
    entries:List[Entry] = None # !! will be filled when feed data is retrieved. Will be an array of 'formated_entries'
    def __init__(self, name, import_feeds_from=None, keep_only=None):
        self.name, self.import_feeds_from, self.keep_only = name, import_feeds_from, keep_only
    def __str__(self):
        #print('-', self.name, self.import_feeds_from, self.keep_only)
        return str([str(feed) for feed in self.feeds])








class RSC:

    #---------------------- 
    name: str = None
    categories: List[Category] = None
    description: str = None
    max_age_minutes: int = None
    last_update = None #!! will be filled when feed data is retrieved

    #------------------------------------        
    def __str__(self):
        #print(self.name, self.description, self.max_age_minutes)
        return str([str(c) for c in self.categories])
    
    def __init__(self, rsc_file, recur=0):
        if recur>100:
            raise Exception('Infinite loop ? more than 100 recursive rsc parse')
        content = urllib.request.urlopen(rsc_file).read() if rsc_file.startswith('http') else open(rsc_file).read()
        rsc = yaml.load( content, yaml.SafeLoader)
        self.name, self.description, self.max_age_minutes = rsc['name'], rsc.get('description'), rsc.get('max_age_minutes')
        self.categories = [] 
        for category in rsc['categories']:
            parsed_category = Category(category.get('name'), category.get('import_feeds_from'), category.get('keep_only'))
            parsed_category.feeds = self.get_feeds_of_category(category) 
            self.categories.append(parsed_category)
            
            
    def _get_raw_posts(self):
        """
        Retrieve not filtered posts for this rsc conf. 
        """
        inputs = []
        for category in self.categories:
            inputs += [ feed.inpuut for feed in category.feeds]
        raw = retrieve_inputs(inputs)
        return raw
    
    def fill_rsc(self):
        self._fill_rsc_without_thumbnails()
        for cat in self.categories:
            for entry in cat.entries:
                entry.try_to_add_image()
    
    def _fill_rsc_without_thumbnails(self):
        """
        Fill the Category entries of the RSC object with filtered and ordered posts (entries), BUT without thumbnails.
        Steps : 
        1. get raw posts
        2. filter
        3. log stats
        4. sort
        """
        #if pas google news : ajouter la source 
        self.last_update = datetime.datetime.now().strftime("%d/%m/%y %H:%M") 
        raw_results = self._get_raw_posts()
        for category in self.categories:
            category.entries = []
            for feed in category.feeds:
                if feed.inpuut not in raw_results:
                    info(f"le feed {feed.name} n'a pas donné de réponse")
                    continue
                data = raw_results[feed.inpuut]
                stats = {'entries':0, 'no_error':0, 'passed_feed_keep_filter':0, 'passed_category_keep_filter': 0, 'passed_max_age_filter':0}

                for raw_entry in data.entries:
                    stats['entries'] +=1
                    try:
                        entry = Entry(raw_entry, feed.name)
                    except:
                        error(f'Error while parsing an entry of {feed.name}')
                        continue
                    try:
                        debug(raw_entry['title'])
                        #applying filters
                        passed_feed_keep_filter = True if feed.keep_only == None else entry.keep_filter(feed.keep_only)
                        passed_category_keep_filter = True if category.keep_only == None else entry.keep_filter(category.keep_only)
                        passed_max_age_filter = True if self.max_age_minutes == None else entry.max_age_filter(self.max_age_minutes)
                        if passed_feed_keep_filter and passed_category_keep_filter and passed_max_age_filter: 
                            category.entries.append(entry)
                        #print(feed.name, formated_entry['title'], max_age_filter(self, entry), formated_entry['published_key'], formated_entry['published'])
                        stats['no_error'] +=1
                        stats['passed_feed_keep_filter'] += 1 if passed_feed_keep_filter else 0
                        stats['passed_category_keep_filter'] += 1 if passed_category_keep_filter else 0
                        stats['passed_max_age_filter'] += 1 if passed_max_age_filter else 0
                        #print(feed.name, entry.published_key)
                    except:
                        error(f'Error while filtering an entry of {feed.name}')
                        continue
                info(f"{feed.name} stats: {stats['entries']} entries, {stats['no_error']} no_error, {stats['passed_feed_keep_filter']} passed_feed_keep_filter, " +\
                      f"{stats['passed_category_keep_filter']}: passed_category_keep_filter, {stats['passed_max_age_filter']}: passed_max_age_filter")
            #newer first:
            (category.entries).sort(key=lambda x: x.published, reverse=True)
    
    

    def get_feeds_of_category(self, category_conf: Dict):
        if 'import_feeds_from' in category_conf:
            origin = category_conf['import_feeds_from']
            imported_rsc = RSC(origin.split(':')[0] if ':' in origin else origin)
            imported_category_name = origin.split(':')[1] if ':' in origin else category_conf['name']
            info('Category imported:' + imported_category_name)
            #print(imported_category_name)
            imported_category = (list(filter(lambda c:c.name==imported_category_name, imported_rsc.categories)))[0] 
            #todo erreur propre si le nom de catégory n'existe pas 
            return imported_category.feeds
        feeds: List[Feed] = []
        for i, feed in enumerate(category_conf['feeds']):
            possibles_names = []
            for entry_key in feed.keys():
                if entry_key not in KEYWORDS.values():
                    possibles_names.append(entry_key)
            if len(possibles_names) == 0:
                error(f'The input number {i} has no name')
                continue
            if len(possibles_names)>1:
                error(f'Category: {category_conf["name"]} : The input number {i} has {len(possibles_names)} possible names : {",".join(possibles_names)}')
                continue
            feed_name = possibles_names[0]
            feeds.append(Feed(feed_name, feed[feed_name], feed.get('keep_only')))
        return feeds 
    
    
    def to_dict(self):
        import copy
        formated_posts = copy.deepcopy(self)
        d = formated_posts.__dict__
        d['categories'] = [cat.__dict__ for cat in d['categories']]
        for cat in d['categories']:
            cat['feeds'] = [f.__dict__ for f in cat['feeds']]
            if 'entries' in cat.keys():
                cat['entries'] = [f.__dict__ for f in cat['entries']] 
        return d

    def to_json(self):
        import json
        def json_serial(obj):
            """JSON serializer for objects not serializable by default json code"""
            if isinstance(obj, (datetime.datetime, date)):
                return obj.isoformat()
            raise TypeError ("Type %s not serializable" % type(obj))
        return json.dumps(self.to_dict(), default=json_serial)






#-------------------- interprete rsc



def print_formated_posts(formated_posts):
    """
    """
    for category in formated_posts.categories:
        print('---------------', category.name)
        for post in category.entries:
            print(post.published, post.source, '---', post.title)
            print(post.url)
            #print(post.summary)
            print()


#---------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    #TODO : aller chercher les images
    #TODO : template simple à base de python
    #TODO : astro build
    #TODO : gérer le cas sitemap

    #p = Parsed_rsc("/Users/nicolas/Documents/dev/ernestine/ernestine2/input/indeps_fact_tribunes.rsc")
    p = RSC("https://raw.githubusercontent.com/nicolasgallandpro/ernestine-data/main/medias_indeps.rsc")
    
    #p = Parsed_rsc("/Users/nicolas/Documents/dev/ernestine/ernestine-data/science.rsc")
    str(p)
    str(p)
    raw = get_raw_posts(p)
    #rsc_conf = parse_rsc_file("/Users/nicolas/Documents/dev/ernestine/ernestine2/input/medias_indeps.rsc")
    #pprint(rsc_conf)

    #raw = get_raw_posts(rsc_conf)
    #print(raw.keys())

    formated_posts = p._fill_rsc_without_thumbnails() 
    print_formated_posts(formated_posts) 
    