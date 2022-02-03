version: 0.1
name: science
description: toute l'actu de la science, en fr et en
max_age_minutes: 1440
categories:
  - name: 'fact_checking'
    feeds:
      - 'les decodeurs - le monde' : 'https://www.lemonde.fr/les-decodeurs/rss_full.xml'
      - 'checknews - libé' : 'https://www.liberation.fr/arc/outboundfeeds/collection/accueil-une/?outputType=xml'
        keep_only: 'checknews in url'
      - 'les surligneurs' : 'https://lessurligneurs.eu/feed/'
      - 'fact checking - rtl' : 'https://www.rtl.fr/podcast/fact-checking.xml'
      - 'le vrai du faux - rf' : 'http://radiofrance-podcast.net/podcast09/rss_12249.xml'
      - "l'instant detox" : 'https://www.youtube.com/channel/UCRAbwEqGDnUBt_gPOkplGBA/videos'
      - 'defakator' : 'https://www.youtube.com/channel/UCU0FhLr6fr7U9GOn6OiQHpQ'
      - 'desintox - arte' : 'https://www.youtube.com/playlist?list=PL3t1ytKnk4hVrv2H-rTSPnySNdqr2CuXL'
