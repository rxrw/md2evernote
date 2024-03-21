import base64
from bs4 import BeautifulSoup
import hashlib
from markdown2 import Markdown

markdowner = Markdown()

class NoteGenerator:

    def __init__(self, writer):
        self.writer = writer

    def generate(self, title, content, created, updated, tags):
        html = markdowner.convert(content)
        html, resources = self.parse_html(html)
        return f"""<note>
    <title>{title}</title>
    <created>{created}</created>
    <updated>{updated}</updated>
    {self.generate_tags(tags)}
    <note-attributes>
        <author>M2ToEverNote</author>
        <source>desktop.win</source>
    </note-attributes>
    <content>
        <![CDATA[<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<!DOCTYPE en-note SYSTEM "http://xml.evernote.com/pub/enml2.dtd"><en-note>{html}</en-note>]]>
    </content>
    {"".join(resources)}
</note>"""

    def generate_tags(self, tags: list):
        tag_strings = []
        for tag in tags:
            tag_strings += f"""<tag>{tag}</tag>"""
        return ''.join(tag_strings)

    def parse_html(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        images = soup.find_all('img')
        if not images:
            return html, []
        resources = []
        for image in images:
            image_src = image['src']
            image_resource, info = self.generate_images(image_src)
            en_media_tag = soup.new_tag("en-media", type="image/jpeg", hash=info["hash"])
            image.replace_with(en_media_tag)
            resources.append(image_resource)
        return str(soup), resources

    def generate_images(self, file_path):
        base64_file = self.get_base64(file_path)
        return f"""
            <resource>
                <data encoding="base64">
                    {base64_file}
                </data>
                <mime>image/jpeg</mime>
            </resource>
            """, {
            "hash": hashlib.md5(base64_file.encode()).hexdigest(),
            "file_path": file_path
        }

    def get_base64(self, file_path):
        with open(file_path, "rb") as file:
            return base64.b64encode(file.read()).decode()
