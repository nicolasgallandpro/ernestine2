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

def parse_rsc_file(rsc_file, recur=0):
    """
    - retrieve rsc file in local disk or on the web
    - check rsc format
    - add 'inpuut' and 'name' entries to each feed entry
    """
    if recur>100:
        raise Exception('Infinite loop ? more than 100 recursive rsc parse')
    content = urllib.request.urlopen(rsc_file).read() if rsc_file.startswith('http') else open(rsc_file).read()
    rsc = yaml.load( content, yaml.SafeLoader)
    parsed = copy.deepcopy(rsc)
    parsed['categories'] = []
    #pprint(rsc)

    def get_feeds_of_category(category):
        if 'import_feeds_from' in category:
            origin = category['import_feeds_from']
            imported_rsc = parse_rsc_file(origin.split(':')[0] if ':' in origin else origin)
            imported_category_name = origin.split(':')[1] if ':' in origin else category['name']
            imported_category = (list(filter(lambda c:c['name']==imported_category_name, imported_rsc['categories'])))[0] 
            #todo erreur propre si le nom de catégory n'existe pas 
            return imported_category['feeds']
        feeds = []
        for i, feed in enumerate(category['feeds']):
            possibles_names = []
            for entry_key in feed.keys():
                if entry_key not in KEYWORDS.values():
                    possibles_names.append(entry_key)
            if len(possibles_names) == 0:
                raise Exception(f'The input number {i} has no name')
            if len(possibles_names)>1:
                raise Exception(f'Category: {category["name"]} : The input number {i} has {len(possibles_names)} possible names : {",".join(possibles_names)}')
            parsed_feed = copy.deepcopy(feed)
            feed_name = possibles_names[0]
            del parsed_feed[feed_name]
            parsed_feed['inpuut'] = feed[feed_name]
            parsed_feed['name'] = feed_name
            feeds.append(parsed_feed)
        return feeds

    # name
    if 'name' not in rsc:
        raise Exception("The rsc file as no 'name' entry")
    for category in rsc['categories']:
        parsed_category = copy.deepcopy(category)
        parsed_category['feeds'] = get_feeds_of_category(category) 
        parsed['categories'].append(parsed_category)
           
    return parsed


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
    inputs = []
    for category in rsc_conf['categories']:
        inputs += [ feed['inpuut'] for feed in category['feeds']]
    raw = retrieve_inputs(inputs)
    return raw


def format_entry(entry, feed):
    """
    Helper : Create an object with unified informations (title, source, ...)
    """
    link = entry['link'] 
    url = link if type(link)==type('') else link['href']  
    return {
        'source': entry['source']['title'] if 'source' in entry else feed['name'] if type(link)==type('') else link['name'], 
        'url': url,
        'title': entry['title'],
        'summary': entry['summary'],
        'id': entry['id'],
        'published': entry['published'],
        'author': entry['author'] if 'author' in entry else None,
        'image': entry['media_content'] if 'media_content' in entry and \
            ('jpg' in entry['media_content'] or 'jpeg' in entry['media_content']) else None
    }
def entry_keep_filter(keep_filter, f):
    """
    Helper : eval keep filter. 
    Args : feed, f (=formated entry)
    """
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
    if KEYWORDS['max_age'] not in rsc_conf : 
        return True
    age_s = (datetime.datetime.utcnow().replace(tzinfo=None) - dateutil.parser.parse(entry['published']).replace(tzinfo=None)).total_seconds()
    return (age_s/60) < rsc_conf[KEYWORDS['max_age']]

#-------------------- interprete rsc
def prepare_curation_data_without_thumbnails(rsc_conf, raw_results):
    """
    Makes a well formated object with categories, sources, ordered posts
    """
    #if pas google news : ajouter la source 
    rsc_conf['last_update'] = datetime.datetime.now().strftime("%d/%m/%y %H:%M") 
    for category in rsc_conf['categories']:
        category['entries'] = []
        for feed in category['feeds']:
            data = raw_results[feed['inpuut']]
            for entry in data['entries']:
                formated_entry = format_entry(entry, feed)
                debug(entry['title'])
                #applying filters
                feed_keep_filter_passed = True if KEYWORDS['keep_filter'] not in feed else entry_keep_filter(feed[KEYWORDS['keep_filter']], formated_entry)
                category_keep_filter_passed = True if KEYWORDS['keep_filter'] not in category else entry_keep_filter(category[KEYWORDS['keep_filter']], formated_entry)
                if feed_keep_filter_passed and category_keep_filter_passed and max_age_filter(rsc_conf, entry): 
                    category['entries'].append(formated_entry)
        #newer first:
        (category['entries']).sort(key=lambda x: dateutil.parser.parse(x['published']), reverse=True)
                
    return rsc_conf


def print_formated_posts(formated_posts):
    """
    """
    for category in formated_posts['categories']:
        print('---------------', category['name'])
        for post in category['entries']:
            print(post['published'], post['source'], '---', post['title'])
            print(post['url'])


#---------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    from pprint import pprint
    
    rsc_conf = parse_rsc_file("/Users/nicolas/Documents/dev/ernestine/ernestine2/input/example_import.rsc")
    #pprint(rsc_conf)

    raw = get_raw_posts(rsc_conf)
    #print(raw.keys())

    formated_posts = prepare_curation_data_without_thumbnails(rsc_conf, raw) 
    print_formated_posts(formated_posts) 
    #pprint(formated_posts)
    