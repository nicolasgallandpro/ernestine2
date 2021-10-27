import feedparser, feedgen
from icecream import ic

#feed = feedparser.parse('https://waylonwalker.com/rss.xml')
#feed = feedparser.parse('https://usbeketrica.com/rss')
#feed = feedparser.parse('https://datajournalism.com/read/rss/longreads.xml')
feed = feedparser.parse('https://news.google.com/rss/search?q=neolithic')
# https://news.google.com/rss?hl=<LANGUAGE_CODE>&gl=<COUNTRY_CODE>&ceid=<COUNTRY_CODE>:<LANGUAGE_CODE>

print()
print("-------- keys of feed")
for key in feed.keys():
    print (key)

print("-------- keys of an entry")
for key in feed.entries[0].keys():
    print(key)

print("------- exemples de valeurs")
ic(feed.headers)
e = feed.entries[0]
ic(e.summary[0:100])
ic(e.title, e.get("author"), e.get("authors"), e.get("author_detail"), e.get("publisher"), e.get('source'), e.link, e.published, e.published_parsed, e.id)

#print (entry.title, entry.href)


#----------------------------------------
#pour générer : https://github.com/lkiesow/python-feedgen

#urls = ['https://waylonwalker.com/rss',
#        'https://joelhooks.com/rss.xml',
#        'https://swyx.io/rss.xml',
#    ]
#feeds = [feedparser.parse(url)['entries'] for url in urls]

#import dateutil.parser
#feed = [item for feed in feeds for item in feed]
#feed.sort(key=lambda x: dateutil.parser.parse(x['published']), reverse=True)


#---------- feedgen
#from feedgen.feed import FeedGenerator
#fg = FeedGenerator()
#fg.id('http://lernfunk.de/media/654321')
#fg.title('Some Testfeed')
#fg.author( {'name':'John Doe','email':'john@example.de'} )
#fg.link( href='http://example.com', rel='alternate' )
#fg.logo('http://ex.com/logo.jpg')
#fg.subtitle('This is a cool feed!')
#fg.link( href='http://larskiesow.de/test.atom', rel='self' )
#fg.language('en')

#atomfeed = fg.atom_str(pretty=True) # Get the ATOM feed as string
#rssfeed  = fg.rss_str(pretty=True) # Get the RSS feed as string
#fg.atom_file('atom.xml') # Write the ATOM feed to a file
#fg.rss_file('rss.xml') # Write the RSS feed to a file

#fe = fg.add_entry()
#fe.id('http://lernfunk.de/media/654321/1')
#fe.title('The First Episode')
#fe.link(href="http://lernfunk.de/feed")
#-----------------
