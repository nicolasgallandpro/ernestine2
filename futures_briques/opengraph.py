from pprint import pprint
import requests
from bs4 import BeautifulSoup

url = "https://dev.to/magesh236/open-graph-protocol-analyzer-4dk0"
#url = "https://realpython.com/python-redis/#example-pyhatscom"
r = requests.get(url=url)
soup = BeautifulSoup(r.text, 'html.parser')
print(soup.find('meta', attrs={'property': 'og:image'})['content'])
