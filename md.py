from datetime import datetime

import yaml
import time
import os

import markdown

from utils import writer

content_root = os.environ.get("CONTENT_ROOT", "./content")
output_file = os.environ.get("OUTPUT_FILE", "./output.enex")


def do_upload_tree():
    enex_writer = writer.Writer(output_file)
    for root, dirs, files in os.walk(content_root):
        for file in files:
            # get extension of file
            ext = os.path.splitext(file)[1]
            if ext == ".md":
                key = os.path.join(root, file)
                # dirname is the folder name of the file
                note = upload_detail(key)
                enex_writer.write(note)
    enex_writer.close()


def upload_detail(file):
    with open(file, "r", encoding="utf-8") as mdFile:
        md_str = mdFile.read()
        md_chunks = md_str.split("---")
        info = yaml.load(md_chunks[1], Loader=yaml.FullLoader)
        page_name = info['title']
        html = markdown.markdown('---'.join(md_chunks[2:]), output_format='xhtml')

        if 'lastmod' in info:
            modified = info.get('lastmod')
            if modified is str:
                modified = time.strptime(modified, "%Y-%m-%dT%H:%M:%S.%fZ")
                modified = time.strftime("%Y%m%dT%H%M%SZ", modified)
            elif modified is datetime:
                modified = datetime.strftime(modified, "%Y%m%dT%H%M%SZ")

        if 'date' in info:
            date = info.get('date')
            if date is str:
                date = time.strptime(date, "%Y-%m-%dT%H:%M:%S.%fZ")
                date = time.strftime("%Y%m%dT%H%M%SZ", date)
            elif date is datetime:
                date = datetime.strftime(modified, "%Y%m%dT%H%M%SZ")

        return {
            "content": html,
            "title": page_name,
            "created": date,
            "updated": modified,
            "tags": [],
            "date": date,
        }


if __name__ == "__main__":
    do_upload_tree()
