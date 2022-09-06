# Convert Markdown to Evernote

I have been found for a long time to convert markdown into evernote. But there is no suitable script for me.

So I have to make a script to convert markdown into evernote, just generate a xml file. You can import it into evernote.

My main purpose is to retain the archtype attribute and finally import markdown into notion. The example archtype.md is [here](./archtype.md)

The script is written in python3. You can use it like this:

```bash
pip3 install markdown
export CONTENT_ROOT = /path/to/your/content
export OUTPUT_FILE = /path/to/your/output.enex
python3 md.py
```
