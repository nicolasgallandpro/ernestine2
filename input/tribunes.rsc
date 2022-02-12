version: 0.1
name: Tribunes
description: Tribunes
max_age_minutes: 1440  #1440 min = 24h
categories:
  - name: 'tribunes'
    feeds:
      - 'google news tribunes' : 'googlenews-fr-fr: tribune'
        'keep_only': "'tribune' not in source and 'stade' not in title"
      - 'tribunes du Monde' : 'https://www.lemonde.fr/idees-tribunes/rss_full.xml'
      - 'thikerview' : 'https://www.youtube.com/channel/UCQgWpmt02UtJkyO32HGUASQ'