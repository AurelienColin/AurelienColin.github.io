import glob
import json
import os
from datetime import datetime

# -----------------------------------------------------------------------------

prefix = """<!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>The Digital Barnacle</title>
        <link rel="icon" href="res/kaggle.png">
        <link rel="stylesheet" type="text/css" href="styles.css">
        <script src="script.js"></script>
    </head>
    <body>
        <iframe src="menu.html" frameborder="0" style="width: 250px; right: 10px; position: fixed; height:100%"></iframe>'
"""

suffix = """
    <div class="cover">
        <img src="res/default_cover.png" id="coverImage">'
    </div>

    <iframe src="bottom.html" frameborder="0" style="height:50px; width:500px; bottom: 0px; margin: auto; position: relative;"></iframe>
</body>
</html>
"""

for filename in glob.glob('res/*/*.json'):
    out_filename = os.path.split(os.path.splitext(filename)[0])[1] + '.html'
    print('Generating', out_filename)

    with open(filename, 'r') as file:
        data = json.load(file)

    lines = [prefix]

    k = 0
    for section_key, section_values in data.items():
        lines += [
            f'    <div class ="part">',
            f'        <h1>',
            f'            {section_key}',
            f'        </h1>'
        ]
        for key, values in section_values.items():
            k += 1
            href = values.get('href', '')
            p = values.get('abstract', '')
            p = p.replace('@{', '<br><br><img class=\"inline\" src=\"')
            p = p.replace('}@', '\"><br>')
            
            cover = values.get('cover', '')
            cover = f' onmouseover="changeImage(\'{cover}\')"' if cover and os.path.exists(cover) else ''

            lines += [
                f'        <div class="container" id="container-{k}"{cover}>',
                f'            <h2>',
                f'                <a href="{href}">{key}</a>',
                f'                <button id="button-{k}"/>',
                f'            </h2>'
            ]

            meta = values.get('meta')
            if meta is not None:
                lines += [
                    f'            <p class="meta">',
                    f'                {meta}',
                    f'            </p>',
                ]

            lines += [
                f'            <p>',
                f'                {p}',
                f'            </p>',
                f'        </div>',
                f'    </div>'
            ]

    lines.append(suffix)
    with open(out_filename, 'w') as file:
        file.write("\n".join(lines))

# -----------------------------------------------------------------------------
print('Generating bottom.html')
with open('bottom.html', 'r') as file:
    line = file.readlines()[1].replace('\n', '')
    version = int(line.split('.')[1]) + 1
print('Version:', version)
now = datetime.now()
lines = [
    f'<!--',
    f'0.{version}',
    f'-->',
    f'<head>',
    f'  <style>',
    '      div {',
    f'          font-size:12px;',
    f'          text-align: center;',
    '      }',
    f'  </style>',
    f'</head>',
    f'<body>',
    f'    <div>',
    f'        Compiled the {now.strftime("%Y-%m-%d")}. Version 0.{version}.',
    f'   </div>',
    f'</body>'
]

with open('bottom.html', 'w') as file:
    file.write("\n".join(lines))


# -----------------------------------------------------------------------------
print('Generating menu.html')
lines = [
"""<head>
    <link rel="stylesheet" type="text/css" href="menu.css">
</head>

<body>
    <a href="https://github.com/AurelienColin/AurelienColin.github.io">
      <img src="res/kaggle.png" width="64">
    </a>
    <table class="menu" cellspacing="5">"""]

filenames = glob.glob('res/*/*.json')
filenames = [filenames[i] for i in [2,3,1,0]]
for filename in filenames:
    shortname = os.path.split(os.path.splitext(filename)[0])[1]
    lines += [
        f'        <tr>',
        f'            <td class="menu_td" onclick="window.open(\'{shortname}.html\', \'_top\')">',
        f'                {shortname[0].upper()}{shortname[1:]}',
        f'                <table class="submenu" cellspacing="5">'
    ]
    with open(filename, 'r') as file:
        data = json.load(file)

    for section_key in data:
        lines +=[
            f'                    <tr>',
            f'                        <td>',
            f'                           {section_key}',
            f'                        </td>',
            f'                    </tr>'
        ]
    lines +=[
        '                </table>',
        '            </td>',
        '        </tr>'
    ]
lines +=[
    '    </table>',
    '</body>'
]
with open('menu.html', 'w') as file:
    file.write("\n".join(lines))
