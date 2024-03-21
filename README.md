# Convert Markdown to Evernote Backup

Help you export your markdown files to Evernote backup files.

I use this to import my markdown files to Evernote, and sync to Notion. This can keep my original created time.

## Advantages

* Keep Origin Format
* Local Image Support
* Easy to Use
* No Need to Install Evernote
* Keep Original Created Time

## Usage
```bash
pip3 install -r requirements.txt
export CONTENT_ROOT = /path/to/your/content
export OUTPUT_FILE = /path/to/your/output.enex
python3 md.py
```

------
Chinese Version
# 将Markdown转换为Evernote备份
    
帮助你将markdown文件导出为Evernote备份文件。

我先将 Markdown 导入到 evernote，然后再从 Notion 导入 Evernote。

这样 Notion Database 中文档的创建时间就是印象笔记的时间，避免导入历史文章时文章的创建时间被设置为当前时间而不可变。

## 优势

* 保持原始格式
* 本地图片支持
* 使用简单
* 无需安装Evernote
* 保持原始创建时间

## 使用
```bash
pip3 install -r requirements.txt
export CONTENT_ROOT = /path/to/your/content
export OUTPUT_FILE = /path/to/your/output.enex
python3 md.py
```