from pathlib import Path
import re
import json

print('---- Scraping Links ----')

api = {}
routes = Path("src/routes")
link_container = []
video_container = []
for x in routes.rglob("*.svx"):
    with open(x, 'r') as f:
        content = f.read()
        flattened = content.replace("\n", " ")
        
        tag_open = False
        url = ''
        name = ''
        for line in content.split('\n'):
            if '<YouTube' in line:
                tag_open = True
            if tag_open == True and 'title' in line:
                name = line
            if tag_open == True and 'url' in line:
                url = line
            if '/>' in line and tag_open == True:
                tag_open = False
                video_container.append({
                    "name" : name[7:-1],
                    "url" : url[5:-1]
                })


        # Extract []() style links
        link_name = "[^]]+"
        link_url = "http[s]?://[^)]+"
        markup_regex = f'\[({link_name})]\(\s*({link_url})\s*\)'

        skip = [
            'of', 'and', 'the', 'to', 'as', 'in', 'for', 'ibuffer', 'on', 'eXchange',
            'https', 'three_anchors', 'means', 'find_tuned',
            'https://en.wikipedia.org/wiki/Moment_(mathematics)',
            'https://Olilarkin.Github.io/Fourses/',
            'olilarkin',
            'github',
            'py'
        ]

        specials = ['you', 'xor', 'mel', 'can']

        for match in re.findall(markup_regex, content):
            name = match[0]
            url = match[1]
            if 'wikipedia' in url:
                if '(' in url:
                    url = url + ')'
            exists = False
            for item in link_container:
                if item["url"] == url:
                    exists = True
            
            if not exists:
                # name processing
                if name[-2:] == "'s":
                    name = name[:-2]
                name = name.replace('`', '')

                if name[0] == '"' and name[-1:] == '"':
                    name = name[1:]
                    name = name[:-1]

                # now capitalise all the big words
                matches = re.findall(r'[\w]+', name)
                for word in matches:
                    if (word not in skip and len(word) >= 4) or word in specials:
                        name = name.replace(word, word[0].upper()+word[1:])
                        if name[0] == "":
                            name = name.replace(word, word[0]+word[1].upper()+word[1:])
                    if word == 's' and len(word) == 1:
                        name = name[0].upper()+name[1:]

                if not '/Projects/' in name and not '/Software' in name:
                    link_container.append({
                        "name" : name,
                        "url" : url
                    })

        # Extract whatever is inbetween <VideoMedia>
        vids_regex = '<VideoMedia(.*?)</VideoMedia>'
        url_regex = 'src="(.*?)"'
        name_regex = "title='(.*?)'"
        iframes = re.findall(vids_regex, flattened)
        for x in iframes:
            url = re.findall(url_regex, x)
            name = re.findall(name_regex, x)
            if url and name:
                video_container.append({
                    "name" : name[0],
                    "url" : url[0]
                })
            else:
                print(f'ERROR: {url}, {name}')

api["links"] = link_container
api["videos"] = video_container

with open("src/data/links.json", "w+") as f:
    json.dump(api, f)

            