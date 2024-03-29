version: 0.1
name: science
description: dataviz and data journalism
max_age_minutes: 10080 # 7 days
categories:
  - name: 'dataviz'
    feeds:
      - "what's new in publishing" : 'https://whatsnewinpublishing.com/feed/'
        'keep_only': "'charts' in text or 'dataviz' in text or 'data visual' in text OR 'data journalism' in text"
      - 'data journalism' : 'https://datajournalism.com/read/rss/longreads.xml'
      #- 'posts medium taggés dataviz (pas toujours très pertinent)' : 'https://medium.com/feed/tag/data-visualization'
      #- 'google news data artist' : 'googlenews-en-en: data artist'
      - 'nightingale' : 'https://medium.com/feed/nightingale'
      - 'flowing data' : 'https://flowingdata.com/feed'
      - 'blog data wrapper' : 'https://blog.datawrapper.de/feed/'
      - 'podcast alberto cairo' : 'https://anchor.fm/s/47aac444/podcast/rss'
      - 'visual capitalist' : 'https://feeds.feedburner.com/visualcapitalist'
