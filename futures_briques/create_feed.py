import feedparser, feedgen
from icecream import ic

#pour générer : https://github.com/lkiesow/python-feedgen

urls = ['https://waylonwalker.com/rss',
        'https://joelhooks.com/rss.xml',
        'https://swyx.io/rss.xml',
    ]
feeds = [feedparser.parse(url)['entries'] for url in urls]

import dateutil.parser
feed = [item for feed in feeds for item in feed]
feed.sort(key=lambda x: dateutil.parser.parse(x['published']), reverse=True)


#---------- feedgen
from feedgen.feed import FeedGenerator
fg = FeedGenerator()
fg.id('http://lernfunk.de/media/654321')
fg.title('Some Testfeed')
fg.author( {'name':'John Doe','email':'john@example.de'} )
fg.link( href='http://example.com', rel='alternate' )
fg.logo('http://ex.com/logo.jpg')
fg.subtitle('This is a cool feed!')
fg.link( href='http://larskiesow.de/test.atom', rel='self' )
fg.language('en')

atomfeed = fg.atom_str(pretty=True) # Get the ATOM feed as string
rssfeed  = fg.rss_str(pretty=True) # Get the RSS feed as string
fg.atom_file('atom.xml') # Write the ATOM feed to a file
fg.rss_file('rss.xml') # Write the RSS feed to a file

fe = fg.add_entry()
fe.id('http://lernfunk.de/media/654321/1')
fe.title('The First Episode')
fe.link(href="http://lernfunk.de/feed")
#-----------------
