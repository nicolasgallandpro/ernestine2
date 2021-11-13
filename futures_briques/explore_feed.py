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

