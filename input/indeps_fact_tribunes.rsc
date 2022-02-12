version: 0.1
name: 'medias indépendants, tribunes, et fact checking'
description: 'medias indépendants, tribunes, et fact checking'
max_age_minutes: 1440  #1440 min = 24h
categories:
  - name: 'tribunes'
    import_feeds_from: '/Users/nicolas/Documents/dev/ernestine/ernestine2/input/tribunes.rsc:tribunes'
  - name: 'medias_independants'
    import_feeds_from: '/Users/nicolas/Documents/dev/ernestine/ernestine2/input/medias_indeps.rsc:medias_indeps'
  - name: 'fact_checking'
    import_feeds_from: '/Users/nicolas/Documents/dev/ernestine/ernestine2/input/fact_checking.rsc:fact_checking'