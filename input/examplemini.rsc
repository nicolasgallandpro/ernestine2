version: 0.1
name: science
description: toute l'actu de la science, en fr et en
max_age_minutes: 1440
formatting:
  - "title": true
  - "author": true
categories:
  - name: 'biologie'
    feeds:
      - 'blog le monde realites biomedicales': https://www.lemonde.fr/blog/realitesbiomedicales/feed/
  - name: 'tribunes'
    feeds:
      - 'google news tribunes' : 'googlenews-fr-fr: tribune'
        'keep_only': "'tribune' not in source"