version: 0.1
name: science
description: toute l'actu de la science, en fr et en
refresh_time: "* * * *"
formatting:
  - "title": true
  - "author": true
feeds:
    - 'le monde pixels': https://www.lemonde.fr/pixels/rss_full.xml
    - 'le monde planete': https://www.lemonde.fr/planete/rss_full.xml
    - 'chaine youtube x': https://www.youtube.com/channel/UCU0FhLr6fr7U9GOn6OiQHpQ
    - 'chaine youtube y': https://www.youtube.com/channel/UC3E2DhYIqnoc6H3WXwTVnlA
    - 'stat news': https://www.statnews.com/feed/
    - 'blog le monde realites biomedicales': https://www.lemonde.fr/blog/realitesbiomedicales/feed/
    - 'nyt science': https://rss.nytimes.com/services/xml/rss/nyt/Science.xml
    - 'podcast x': http://radiofrance-podcast.net/podcast09/rss_14312.xml
    - 'podcast y': http://radiofrance-podcast.net/podcast09/rss_20902.xml   #commentaire 
    - 'google news paleoanthropologie fr': 'googlenews-fr-fr: paléoanthropologie'
    - 'google news tribunes' : 'googlenews-fr-fr: tribune'
      keep_only: "'Tribune de Genève' not in source and 'Tribune de lyon' not in source and 'latribune' not in domain and 'herault-tribune' not in domain"