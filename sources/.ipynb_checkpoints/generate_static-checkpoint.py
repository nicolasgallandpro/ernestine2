from art import text2art
from rsc import *

page_template = """
<!DOCTYPE html>
<html lang="fr">
  <head>
    <meta charset="utf-8">
    <title>Swartz News</title>
    <link rel="stylesheet" href="style.css">
    <script src="script.js"></script>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <meta property="og:title" content="Swartz News" />
    <meta property="og:description" content="L'info de 35 Médias indépendants centralisée en 1 endroit. Mediapart - Blast - Thinkerview - Osons Causer - Off Investigation..." />
    <script type="module" src="https://unpkg.com/ionicons@5.5.2/dist/ionicons/ionicons.esm.js"></script>
    <script nomodule src="https://unpkg.com/ionicons@5.5.2/dist/ionicons/ionicons.js"></script>
  </head>
  <body style="font-family:monospace; font-size: 1.1em">
   {content}
  </body>
</html>
"""

medias = text2art("Swartz").replace(' ','&nbsp;').replace('\n','<br/>\n')
independants = text2art("News").replace(' ','&nbsp;').replace('\n','<br/>\n')
head_template = f"""
<div style="font-size: 0.9em;">
<p>{medias}</p>
</div>
<div style="font-size: 0.9em;">
<p>{independants}</p>
</div>
<div style="font-size: 0.8em;">
<p>------------------------------------</p>
<p>Centralise l'info de <a style="color:black" href="https://github.com/nicolasgallandpro/ernestine-data/blob/main/medias_indeps.rsc">35 médias indépendants</a>. Articles, vidéos, et podcasts</p>
<p>Mediapart - Blast - Thinkerview - Off Investigations - Osons Causer - The Conversation ...</p>
<p>24h d'info brute, sans influence de milliardaires et sans algo. Actualisé toutes les heures </p>
<p>------------------------------------</p>
<br/>
</div>
"""

footer_template = f"""
<br/>
<br/>
<br/>
<a href="https://github.com/nicolasgallandpro/ernestine-data/blob/main/medias_indeps.rsc"><p style="color:black">Liste complète des sources utilisés</p></a>"""

categoty_template = """<p>------------------ {category} ------------------</p>"""

entry_template = """
<p><span  style="color:#FAA2AE">{published}</span> {icon} <a style="color:black; text-decoration-color: #aaaaaa;" href="{url}">{title}<a/> -- <span style="color:#999999;">{source}</span></p>
<p/>
"""

icon_audio = '<ion-icon name="mic-outline"></ion-icon>'
icon_video = '<ion-icon name="videocam-outline"></ion-icon>'
icon_book = '<ion-icon name="book-outline"></ion-icon>'

video_sources = "osons causer,blast,thinkerview,arrêt sur image".split(',')
audio_sources = ['in extenso']

def create_page(rsc, file, show_categories=True):
  p = Parsed_rsc(rsc)
  raw = get_raw_posts(p)
  formated_posts = prepare_curation_data_without_thumbnails(p, raw) 
  out = ""
  for category in formated_posts.categories:
    if show_categories:
        out += categoty_template.format(category=category.name)
    for post in category.entries:
      icon = icon_video if post.source in video_sources else icon_audio if post.source.lower() in audio_sources else icon_book
      out += entry_template.format(title=post.title, published=str(post.published).split('+')[0],\
        source=post.source, url=post.url, icon=icon)
  out = head_template + out
  out = page_template.format(content=out)
  out = out + footer_template

  #print(out)
  f = open(file,'w')
  f.write(out)
  f.close()
  return out
if __name__ == "__main__":
  logging.basicConfig(level=logging.INFO)
  create_page("/Users/nicolas/Documents/dev/ernestine/ernestine2/input/medias_indeps.rsc", "/Users/nicolas/Documents/dev/ernestine/static_v1/output/index.html", show_categories=False)
