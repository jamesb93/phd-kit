from pathlib import Path
import json

print('---- Extracting Structure Of Thesis ----')

def get_heading(line):
    line = line.rstrip()
    line = line.replace('#', '')
    line = line.lstrip()
    return line

def get_url(line):
    line = line.rstrip()
    line = line.replace('#', '')
    line = line.lstrip()
    line = line.lower()
    line = line.replace(' ', '-')
    line = line.replace('.', '')
    if line.startswith('--'):
        line = line.replace('--', '')
    line = line.replace('/', '')
    return line

files = [x for x in Path("src/routes").rglob("*.svx")]
ignores = [
    'acknowledgements',
    'conclusion',
    'content-awareness',
    'copyright',
    'directory',
    'howto',
    'introduction',
    'list-of-interactive-elements',
    'preoccupations',
    'projects',
    'references',
    'submission-materials',
    'tech',
    'references',
    'routes'
]

svx = [x for x in files if x.parent.name not in ignores]

hierarchy = {
    '' : '',
    'howto' : '',
    'submission-materials': '',
    'list-of-interactive-elements' : '',
    'introduction' : '1',
    'preoccupations' : '2', 
    'content-awareness' : '3',
    'stitch-strata' : '4.1',
    'annealing-strategies' : '4.2',
    'refracted-touch' : '4.3',
    'reconstruction-error' : '4.4',
    'interferences' : '4.5',
    'mosh' : '5.1',
    'ftis' : '5.2',
    'reacoma' : '5.3',
    'conclusion' : '6.',
    'copyright' : '',
    'references' : ''
}

structure = {}

for page in svx:
    c = {
        1 : 0,
        2 : 0,
        3 : 0,
        4 : 0,
        5 : 0
    }
    # This translates the relative path inside src/routes
    # intro a structure which treats routes as the root, or ''
    path = str(page.relative_to('src/routes').parent)
    prefix = hierarchy[page.parent.stem]

    # print(page.stem, prefix)
    structure[path] = []
    with open(page) as text:
        lines = text.readlines();
        for line in lines:
            if line.startswith('#'):
                heading = get_heading(line)
                url = get_url(line)
                indent = line.count('#')
                print(heading, indent)

                calculated_heading = ''
                if prefix != '':
                    c[indent] += 1
                    if indent == 1:
                        calculated_heading = f'{prefix} {heading}'
                    elif indent == 2:
                        calculated_heading = f'{prefix}.{c[2]} {heading}'
                    elif indent == 3:
                        calculated_heading = f'{prefix}.{c[2]}.{c[3]} {heading}'
                    elif indent == 4:
                        calculated_heading = f'{prefix}.{c[2]}.{c[3]}.{c[4]} {heading}'
                    elif indent == 5:                    
                        calculated_heading = f'{prefix}.{c[2]}.{c[3]}.{c[4]}.{c[5]} {heading}'
                    for i in range(indent+1, 5):
                        c[i] = 0
                else :
                    calculated_heading = heading

                structure[path].append(
                    {
                        'heading' : calculated_heading,
                        'indent' : indent,
                        'url' : url
                    }
                )
                
with open('src/lib/data/structure.json', 'w') as output:
    json.dump(structure, output)
