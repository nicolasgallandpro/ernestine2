from art import text2art
from rsc import *

page_template = """
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://unpkg.com/alpinejs" defer></script>
    <title>Swartz.news</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css?family=Open+Sans:300,400|Playfair+Display|Playfair+Display+SC|Roboto:300,400&display=swap" rel="stylesheet">
</head>
<body>
    <style>
    p {
      font-family: 'Open Sans', sans-serif;
     font-weight: 300;
    }
    h2 {
     font-family: 'Playfair Display', sans-serif;
     font-weight: 600;
    }
    .playfair{ font-family: 'Playfair Display SC'}
    .roboto { font-family: 'Roboto';font-weight: 300;}
        
    </style>
    <div class="container mx-auto px-6 md:px-40">

        <div class="playfair md:text-6xl text-5xl mb-4 pt-6">
            ___TITLE___
        </div>
        
        <p class="mb-6">___DESCRIPTION___</p>
       
        <main class="py-6" x-data="{categories : []}"
        x-init="fetch('https://swartz.news/___JSON___')
            .then(response=> {
                if (!response.ok) alert(`Something went wrong: ${response.status} - ${response.statusText}`)
                return response.json()
            })
            .then(data => categories = data.categories)">

            <template x-for="entry in categories[0].entries">
                <div class="mb-12">
                    <div class="flex flex-col md:flex-row w-full lg:w-12/12">
                        <div class="md:mr-4 mb-2 md:mb-0 md:w-4/12 ">
                            <a class="bg-gray-100" :href="entry.url">
                                <img style="width:640;height:360;" class="object-cover h-56 w-96 rounded-lg mb-3 hover:opacity-70 transition duration-300 ease-in-out" alt="" :src="entry.image">
                            </a>
                        </div>
                        <div class="flex-1">
                            <a :href="entry.url" >
                                <h2 class="text-xl mb-1 playfair" x-text="entry.title"></h2>
                            </a>
                            <div class="p-1 px-3 mr-1 mb-1 inline-block text-xs font-mono rounded text-blue-800 hover:bg-blue-200 hover:text-blue-800 transition duration-300 ease-in-out">
                                 <span x-text="entry.published.split('T')[0]"></span> - <span x-text="entry.source"></span>  
                            </div>
                            <p class="text-sm text-gray-600 mb-4 roboto" x-text="entry.summary"></p>
                            
                        </div>
                    </div>
                </div>
            </template>
        
        </main>

    </div>


</body>
</html>
"""

icon_audio = '<ion-icon name="mic-outline"></ion-icon>'
icon_video = '<ion-icon name="videocam-outline"></ion-icon>'
icon_book = '<ion-icon name="book-outline"></ion-icon>'

video_sources = "osons causer,blast,thinkerview,arrêt sur image".split(',')
audio_sources = ['in extenso']

def create_page(rsc_filled, basedir, file, title, description, json):
    content = page_template.replace('___TITLE___',title).replace('___DESCRIPTION___',description)\
                .replace('___JSON___',json)
    #print(out)
    
    #html
    f = open(basedir+file,'w')
    f.write(content)
    f.close()
    
    #json
    f = open(basedir+json, "w")
    f.write(rsc_filled.to_json())
    f.close()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    create_page("/Users/nicolas/Documents/dev/ernestine/ernestine2/input/medias_indeps.rsc", "/Users/nicolas/Documents/dev/ernestine/static_v1/output/index.html", show_categories=False)
