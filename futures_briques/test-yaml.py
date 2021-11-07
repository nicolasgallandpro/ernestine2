from yaml import load
from pprint import pprint
import requests


url = 'https://raw.githubusercontent.com/nicolasgallandpro/ernestine-data/main/tribunes.rsc'
r = requests.get(url, allow_redirects=True).content

pprint(load(r))

