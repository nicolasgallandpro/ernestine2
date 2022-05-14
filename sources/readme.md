!!!! todo : get_raw_posts doit retourner des Entry, pour ne pas mélanger tout (et prendre une liste de catégories en entrée)
!!! mettre get_raw_posts à l'intérieur de prepare_curation_data_without_thumbnails
!!! mettre prepare_curation_data_without_thumbnails dans son propre fichier (execute_rsc) ? 
!!! renommer prepare_curation_data_without_thumbnails en fill_rsc_object, et ajouter les thumbnails ?

# rsc.py
....
### class Parsed_rsc:
* name: str 
* categories: List[Category] 
* description: str 
* max_age_minutes: int 
* last_update                  #!! will be filled when feed data is retrieved

### class Category:
* name: str 
* feeds: List[Feed] 
* import_feeds_from: str 
* keep_only:str 
* entries:List[Entry]       # !! will be filled when feed data is retrieved. Will be an array of 'formated_entries'

### class Feed
* name: str = None
* inpuut: str = None
* keep_only:str = None

### def get_raw_posts(rsc_conf: Parsed_rsc):
return not filtered entries for all rsc feeds (multithreaded)

### def prepare_curation_data_without_thumbnails(rsc_conf: Parsed_rsc, raw_results):
Input : Parsed_rsc Object + raw posts
Output : a filled and ready Parsed_rsc object, with the categories filled with ordered and filtered entries (posts)


# entries.py
....
### class Entry:
A post entry of rss or sitemap
* source: str; 
* url: str; 
* title: str; 
* summary: str = None; 
* id: str = None; 
* published = None; 
* s_spublished: str = None; 
* published_key: str = None; 
* author: str= None; 
* image: str = None

* def keep_filter(self, keep_filter: str) -> bool
* def max_age_filter(self, max_age_minutes: int) -> bool