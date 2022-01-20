version: 0.1
name: science
description: toute l'actu de la science, en fr et en
max_age_minutes: 1440  #1440 min = 24h
formatting:
  - "title": true
  - "author": true
categories:
  - name: 'paleoanthropologie'
    feeds:
      - 'le monde pixels': https://www.lemonde.fr/pixels/rss_full.xml
      - 'le monde planete': https://www.lemonde.fr/planete/rss_full.xml
      - 'chaine youtube x': https://www.youtube.com/channel/UCU0FhLr6fr7U9GOn6OiQHpQ
      - 'chaine youtube y': https://www.youtube.com/channel/UC3E2DhYIqnoc6H3WXwTVnlA
      - 'stat news': https://www.statnews.com/feed/
      - 'nyt science': https://rss.nytimes.com/services/xml/rss/nyt/Science.xml
      - 'podcast x': http://radiofrance-podcast.net/podcast09/rss_14312.xml
      - 'podcast y': http://radiofrance-podcast.net/podcast09/rss_20902.xml   #commentaire 
      - 'google news paleoanthropologie fr': 'googlenews-fr-fr: paléoanthropologie'
  - name: 'biologie'
    feeds:
      - 'blog le monde realites biomedicales': https://www.lemonde.fr/blog/realitesbiomedicales/feed/
  - name: 'tribunes'
    feeds:
      - 'google news tribunes' : 'googlenews-fr-fr: tribune'
        'keep_only': "'tribune' not in source"