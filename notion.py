from datetime import datetime

import time
import os

import markdown

content_root = os.environ.get("CONTENT_ROOT", ".")
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

def find_config(content: str):
    config = {}
    content = []
    for index, line in enumerate(content.splitlines()):
        if index == 0:
            # remove # in the left
            config["title"] = line[2:].strip()
        elif index >= 2 or index < 5:
            key, value = line[1:].split(":", 1)
            config[key.strip().lower()] = value.strip()
        else:
            content.append(line)

    return config, "\n".join(content)


def upload_detail(file, dirname):

    with open(file, "r", encoding="utf-8") as mdFile:
        #Preprocess the Markdown frontmatter into yaml code fences
        mdStr = mdFile.read()
        info, content = find_config(mdStr)
        pageName = info['title']
        # mdFile = io.StringIO(mdStr)
        html = markdown.markdown(content, output_format='xhtml')
        # August 24, 2019 8:22 PM
        date = time.strptime(info['created at'], "%B %d, %Y %I:%M %p")
        date = time.strftime("%Y%m%dT%H%M%SZ", date)

        modified = info.get('updated at')
        if modified is not None:
            # 2022-01-21T09:49:21.727Z
            modified = time.strptime(info['created at'], "%B %d, %Y %I:%M %p")
            modified = time.strftime("%Y%m%dT%H%M%SZ", modified)
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

if __name__ == "__main__":
    do_upload_tree()