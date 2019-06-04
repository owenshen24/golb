import os
import json
import time
import re
import PyRSS2Gen
from urllib.parse import quote
from datetime import datetime
from jinja2 import Environment, FileSystemLoader
from markdown2 import markdown

CONFIG_PATH = "metadata/config.json"
OPTIONS = [
    "posts",
    "muse"
]
CONFIG = {}
LAST_UPDATED = None



def updateTime():
    with open(CONFIG_PATH, 'r') as infile:
        config = json.load(infile)
        global LAST_UPDATED
        LAST_UPDATED = config['last-updated']
    config['last-updated'] = time.time()
    with open(CONFIG_PATH, 'w') as infile:
        json.dump(config, infile, indent=4)



def loadConfig(options):
    with open(CONFIG_PATH, 'r') as infile:
        global CONFIG
        CONFIG = json.load(infile)["config"][options]



def extractText(text):
    _meta_data_newline = re.compile("^\n", re.MULTILINE)
    _meta_data_pattern = re.compile(r'^(?:---[\ \t]*\n)?(.*:\s+>\n\s+[\S\s]+?)(?=\n\w+\s*:\s*\w+\n|\Z)|([\S\w]+\s*:(?! >)[ \t]*.*\n?)(?:---[\ \t]*\n)?', re.MULTILINE)
    metadata_split = re.split(_meta_data_newline, text, maxsplit=1)
    metadata_content = metadata_split[0]
    match = re.findall(_meta_data_pattern, metadata_content)
    if not match:
        return text
    tail = metadata_split[1]
    return tail



# Rename new posts to be TITLE#{NUM}
def updatePostNames(id):
    ID_COUNT = id
    for post in os.listdir(CONFIG['CONTENTS_DIR']):
        file_path = os.path.join(CONFIG['CONTENTS_DIR'], post)
        # Skip subdirectories
        if os.path.isdir(file_path):
            continue
        if '#' not in file_path:
            with open(file_path, 'r+') as f:
                post_text = f.read()
                parsed_file = markdown(post_text, extras=['metadata'])
                anchor = quote(parsed_file.metadata['title'].replace(' ', '-'))
            ID_COUNT += 1
            new_file_path = CONFIG['CONTENTS_DIR'] + anchor + '#' + str(ID_COUNT) + '.md'
            os.rename(file_path, new_file_path)
    return(ID_COUNT)



# Update Posts Index with all posts:
def updateIndex(POSTS_LIST, sort_date):
    # Sort descending date
    if (sort_date):
        POSTS_LIST = [POSTS_LIST[p] for p in sorted(
            POSTS_LIST, key=lambda x: POSTS_LIST[x]['last-updated'],
            reverse=True
        )]
    # Else, sort by descending ID
    else:
        POSTS_LIST = [POSTS_LIST[p] for p in sorted(
            POSTS_LIST, key=lambda x: int(POSTS_LIST[x]['id']),
            reverse=True
        )]
    env = Environment(loader=FileSystemLoader(CONFIG['TEMPLATE_DIR'])) 
    index_html = env.get_template(CONFIG["INDEX_TEMPLATE_PATH"]).render(posts = POSTS_LIST)
    with open (CONFIG['OUTPUT_DIR'] + 'index.html', 'w') as output:
        output.write(index_html)



# Updates RSS feed
def updateRSS(CONFIG, POSTS_LIST, id_as_slug):
    # Sort by descending ID
    rss_items = []
    for p in sorted(
        POSTS_LIST, key=lambda x: int(POSTS_LIST[x]['id']),
        reverse=True
    ):
        if id_as_slug:
            post_link = CONFIG['URL'] + str(POSTS_LIST[p]['id']) + '.html'
        else:
            post_link = CONFIG['URL'] + POSTS_LIST[p]['anchor'] + '.html'
        rss_items.append(
            PyRSS2Gen.RSSItem(
    	        title = POSTS_LIST[p]['title'],
                link = post_link,
                description = POSTS_LIST[p]['summary']
          )
        )
    rss = PyRSS2Gen.RSS2(
        title = "Muse",
        link = CONFIG['URL'],
        description = CONFIG['NAME'],
        lastBuildDate = datetime.now(),
        items = rss_items
    )
    rss.write_xml(open(CONFIG['OUTPUT_DIR']+CONFIG['RSS'], "w"))



def parsePosts(sort_date=False, id_as_slug=False):
    # Load up the POSTS_DICT
    POSTS_DICT = {}
    with open(CONFIG['METADATA_DIR'] + CONFIG['METADATA_DICT'], 'r') as infile:
        POSTS_DICT = json.load(infile)
        ID_COUNT = POSTS_DICT['ID_COUNT']
        OLD_ID_COUNT = ID_COUNT

    # Get last updated time for template
    template_update = max(
        int(os.path.getmtime(CONFIG['TEMPLATE_DIR'] + CONFIG["POST_TEMPLATE_PATH"])), 
        int(os.path.getmtime(CONFIG['TEMPLATE_DIR'] + CONFIG["INDEX_TEMPLATE_PATH"])))

    # Rename files and update ID_COUNT
    ID_COUNT = updatePostNames(ID_COUNT)

    # Start the actual parsing
    for post in os.listdir(CONFIG['CONTENTS_DIR']):
        file_path = os.path.join(CONFIG['CONTENTS_DIR'], post)
        file_update = int(os.path.getmtime(file_path))

        # Skip subdirectories:
        if os.path.isdir(file_path):
            continue
        
        post_id = int(post[post.find('#')+1:post.find('.md')])

        # Check if we updated the template or post or
        # if it's the latest post from last time since the last script run
        # or if we need to backtrack to add prev/next buttons to an older post
        if (template_update > LAST_UPDATED or
            file_update > LAST_UPDATED or
            ((post_id >= OLD_ID_COUNT) and id_as_slug and 
             (post_id != ID_COUNT) and OLD_ID_COUNT != ID_COUNT)):
            
            # Parse file
            with open(file_path, 'r+') as f:
                post_text = f.read()
                post_only = extractText(post_text)
                parsed_file = markdown(post_text, extras=['metadata'])
                title = parsed_file.metadata['title']

                # Remove the old HTML file if it exists:
                if str(post_id) in POSTS_DICT['POSTS'].keys() and not id_as_slug:    
                    anchor = POSTS_DICT['POSTS'][str(post_id)]['anchor']
                    old_file = CONFIG['OUTPUT_DIR'] + anchor +'.html'
                    os.remove(old_file)

                # Get provided summary or first 100 chars of .md file
                if 'summary' in parsed_file.metadata.keys():
                    summary = parsed_file.metadata['summary']
                else:
                    summary = post_only[0:100] + '…'
                
                # Get more metadata
                anchor = quote(title.replace(' ', '-'))
                word_count = len(post_only.split(' '))

                # Replace double dashes with em-dash
                parsed_file = parsed_file.replace('--', '—');

                data = {
                    'title': title,
                    'date': datetime.fromtimestamp(
                    file_update).strftime('%Y-%m-%d %H:%M'),
                    'last-updated': file_update,
                    'anchor': anchor,
                    'summary': summary,
                    'word_count': word_count,
                    'id': post_id
                }
                POSTS_DICT['POSTS'][str(post_id)] = data.copy()

                # Add content to data dict
                data['content'] = parsed_file
                data['summary'] = summary

                # Parse the HTML using Jinja and create the page
                env = Environment(loader=FileSystemLoader(CONFIG['TEMPLATE_DIR'])) 
                post_html = env.get_template(CONFIG["POST_TEMPLATE_PATH"]).render(post = data, 
                    max_num = ID_COUNT)

                # Toggle between id or anchor as file name
                if id_as_slug:
                    post_name = str(post_id)
                else:
                    post_name = str(anchor)

                # Save new HTML file
                with open(CONFIG['OUTPUT_DIR'] + post_name+'.html', 'w') as output:
                    output.write(post_html)

            # Update message
            print("Updated: ", title)

    # Save new POSTS_DICT to metadata
    POSTS_DICT['ID_COUNT'] = ID_COUNT
    with open(CONFIG['METADATA_DIR'] + CONFIG['METADATA_DICT'], 'w') as outfile:
        json.dump(POSTS_DICT, outfile, indent=4)

    updateIndex(POSTS_DICT['POSTS'], sort_date)
    updateRSS(CONFIG, POSTS_DICT['POSTS'], id_as_slug)



# Run script as main
if __name__ == "__main__":
    # Set new timestamp for last-updated
    updateTime()
    
    # Parse MLU
    loadConfig(OPTIONS[0])
    parsePosts()

    # Parse Muse
    loadConfig(OPTIONS[1])
    parsePosts(id_as_slug=True)