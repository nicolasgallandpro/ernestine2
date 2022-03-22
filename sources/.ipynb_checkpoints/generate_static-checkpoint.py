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
    <meta property="og:description" content="Le Google News des medias indépendants/" />
  </head>
  <body style="font-family:monospace; font-size: 1.1em">
   {content}
  </body>
</html>
"""

medias = text2art("Medias").replace(' ','&nbsp;').replace('\n','<br/>\n')
independants = text2art("Independants").replace(' ','&nbsp;').replace('\n','<br/>\n')
head_template = f"""
<div style="font-size: 0.8em;">
<p>{medias}</p>
</div>
<div style="font-size: 0.6em;">
<p>{independants}</p>
</div>
<div style="font-size: 0.8em;">
<p>------------------------------------</p>
<p>Les articles, vidéos, et podcasts publiés par les médias indépendants ces dernières 24 heures </p>
<p>L'info, sans l'influence de milliardaires. Mediapart - Blast - Thinkerview - Off Investigations - Osons Causer - ...</p>
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
<p><span  style="color:#FAA2AE">{published}</span> -- <a style="color:black; text-decoration-color: #aaaaaa;" href="{url}">{title}<a/> -- <span style="color:#999999;">{source}</span></p>
<p/>
"""

def create_page(rsc, file, show_categories=True):
  p = Parsed_rsc(rsc)
  raw = get_raw_posts(p)
  formated_posts = prepare_curation_data_without_thumbnails(p, raw) 
  out = ""
  for category in formated_posts.categories:
    if show_categories:
        out += categoty_template.format(category=category.name)
    for post in category.entries:
      out += entry_template.format(title=post.title, published=str(post.published).split('+')[0],\
        source=post.source, url=post.url)
  out = head_template + out
  out = page_template.format(content=out)
  out = out + footer_template

  #print(out)
  f = open(file,'w')
  f.write(out)
  f.close()
if __name__ == "__main__":
  logging.basicConfig(level=logging.INFO)
  create_page("/Users/nicolas/Documents/dev/ernestine/ernestine2/input/medias_indeps.rsc", "/Users/nicolas/Documents/dev/ernestine/static_v1/output/index.html", show_categories=False)
