version: 0.1
name: science
description: toute l'actu de la science, en fr et en
max_age_minutes: 1440
formatting:
  - "title": true
  - "author": true
categories:
  - name: 'vaccin'
    import_feeds_from: '/Users/nicolas/Documents/dev/ernestine/ernestine2/input/example.rsc:science'
    'keep_only': '"vaccin" in text'
  - name: 'covid'
    import_feeds_from: '/Users/nicolas/Documents/dev/ernestine/ernestine2/input/example.rsc:science'
    'keep_only': '"covid" in text'
  - name: 'biologie' 
    import_feeds_from: '/Users/nicolas/Documents/dev/ernestine/ernestine2/input/example.rsc'
  - name: 'tribunes'
    feeds:
      - 'google news tribunes' : 'googlenews-fr-fr: tribune'
        'keep_only': "'tribune' not in source"