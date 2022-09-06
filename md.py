from datetime import datetime

import yaml
import time
import os

import markdown

content_root = os.environ.get("CONTENT_ROOT", "./content")
output_file = os.environ.get("OUTPUT_FILE", "./output.enex")

def do_upload_tree():
    key_list = {}
    for root, dirs, files in os.walk(content_root):
        for file in files:
            # get extension of file
            ext = os.path.splitext(file)[1]
            if ext == ".md" and file != "_index.md":
                key = os.path.join(root, file)
                # dirname is the folder name of the file
                dirname = os.path.basename(root).split("/")[-1]
                key_list[key] = turn_into_xml(upload_detail(key, dirname))
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(format_enex(key_list))

def upload_detail(file, dirname):

    with open(file, "r", encoding="utf-8") as mdFile:
        #Preprocess the Markdown frontmatter into yaml code fences
        mdStr = mdFile.read()
        mdChunks = mdStr.split("---")
        mdStr = \
f"""```yaml
{mdChunks[1]}
```
{'---'.join(mdChunks[2:])}
"""
        info = yaml.load(mdChunks[1], Loader=yaml.FullLoader)
        pageName = info['title']
        # mdFile = io.StringIO(mdStr)
        html = markdown.markdown('---'.join(mdChunks[2:]), output_format='xhtml')
        # 2021-02-05T09:50:48.000Z
        date = info['date'].strftime("%Y%m%dT%H%M%SZ")

        modified = info.get('lastmod')
        if modified is not None:
            # 2022-01-21T09:49:21.727Z
            if type(modified) == str:
                modified = time.strptime(modified, "%Y-%m-%dT%H:%M:%S.%fZ")
                modified = time.strftime("%Y%m%dT%H%M%SZ", modified)
            elif type(modified) == datetime:
                modified = datetime.strftime(modified, "%Y%m%dT%H%M%SZ")
        else:
            modified = date
        return {
            "content": html,
            "title": pageName,
            "created": date,
            "updated": modified,
            "tags": info['tags'],
            # "category": dirname,
            # "description": info['description'],
        }

def turn_into_xml(content):
    tags = []
    for tag in content['tags']:
        tags += f"""<tag>{tag}</tag>"""
    tags = ''.join(tags)
    return f"""<note>
    <title>{content['title']}</title>
    <created>{content['created']}</created>
    <updated>{content['updated']}</updated>
    {tags}
    <note-attributes>
      <author>纠结当道</author>
      <category>{content['category']}</category>
    </note-attributes>
    <content>
      <![CDATA[<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<!DOCTYPE en-note SYSTEM "http://xml.evernote.com/pub/enml2.dtd"><en-note>{content['content']}</en-note>]]>
    </content>
  </note>"""

def format_enex(klist):
    content = ''.join(klist.values())
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE en-export SYSTEM "http://xml.evernote.com/pub/evernote-export4.dtd">
<en-export export-date="20221005T060942Z" application="Evernote" version="10.44.8">{content}
</en-export>"""