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
  </head>
  <body style="font-family:monospace">
   {content}
  </body>
</html>
"""

medias = text2art("Medias").replace(' ','&nbsp;').replace('\n','<br/>\n')
independants = text2art("Independants").replace(' ','&nbsp;').replace('\n','<br/>\n')
head_template = f"""
<p>{medias}</p>
<p>{independants}</p>
<p>------------------------------------</p>
<p>Les articles, vidéos, et podcasts publiés par les médias indépendants ces dernières 24 heures </p>
<p>Certifié 100% sans influence de milliardaire et lobbys industriels</p>
<p>------------------------------------</p>
<br/>
"""

footer_template = f"""
<br/>
<br/>
<br/>
<p>Fait un citoyen lambda """

categoty_template = """<p>------------------ {category} ------------------</p>"""

entry_template = """
<p><span  style="color:#FAA2AE">{published}</span> -- <span style="color:gray;">{source}</span> -- <a style="color:black; text-decoration-color: #aaaaaa;" href="{url}">{title}<a/> </p>
<p/>
"""

def create_page(rsc, file, show_categories=True):
  p = Parsed_rsc(rsc)
  raw = get_raw_posts(p)
  formated_posts = prepare_curation_data_without_thumbnails(p, raw) 
  out = ""
  for category in formated_posts.categories:
    #out += categoty_template.format(category=category.name)
    for post in category.entries:
      out += entry_template.format(title=post.title, published=str(post.published).split('+')[0],\
        source=post.source, url=post.url)
  out = head_template + out
  out = page_template.format(content=out)

  print(out)
  f = open(file,'w')
  f.write(out)
  f.close()

if __name__ == "__main__":
  logging.basicConfig(level=logging.INFO)
  create_page("/Users/nicolas/Documents/dev/ernestine/ernestine2/input/medias_indeps.rsc", "/Users/nicolas/Documents/dev/ernestine/static_v1/output/index.html", show_categories=False)
