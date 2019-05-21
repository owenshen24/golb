import os
import json
import time
import re
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


def parsePosts(sort_date=False, id_as_slug=False):
    # Define path variables
    CONTENTS_DIR = CONFIG['CONTENTS_DIR']
    METADATA_DIR = CONFIG['METADATA_DIR']
    POSTS_DICT_FILE = CONFIG['METADATA_DICT']
    OUTPUT_DIR = CONFIG['OUTPUT_DIR']
    TEMPLATE_DIR = CONFIG['TEMPLATE_DIR']
    POST_TEMPLATE = CONFIG["POST_TEMPLATE_PATH"]
    INDEX_TEMPLATE = CONFIG["INDEX_TEMPLATE_PATH"]

    # Load up the POSTS_DICT
    POSTS_DICT = {}
    with open(METADATA_DIR + POSTS_DICT_FILE, 'r') as infile:
        POSTS_DICT = json.load(infile)
        ID_COUNT = POSTS_DICT['ID_COUNT']

    # Get last updated time for template
    template_update = max(
        int(os.path.getmtime(TEMPLATE_DIR + POST_TEMPLATE)), 
        int(os.path.getmtime(TEMPLATE_DIR + INDEX_TEMPLATE)))

    # Iterate through all posts
    for post in os.listdir(CONTENTS_DIR):
        file_path = os.path.join(CONTENTS_DIR, post)
        file_update = int(os.path.getmtime(file_path))
        post_id = None
        new_file_path = None

        # Skip subdirectories:
        if os.path.isdir(file_path):
            continue

        # Create new entry in POSTS_DICT and rename file if new
        # Otherwise, get existing post_id
        if '#' not in file_path:

            # Rename to be post title
            with open(file_path, 'r+') as f:
                post_text = f.read()
                parsed_file = markdown(post_text, extras=['metadata'])
                anchor = quote(parsed_file.metadata['title'].replace(' ', '-'))
                
            ID_COUNT += 1
            post_id = ID_COUNT
            new_file_path = OUTPUT_DIR + anchor + '#' + str(ID_COUNT) + '.md'
            os.rename(file_path, new_file_path)
        else:
            post_id = int(post[post.find('#')+1:post.find('.md')])

        # Parse the post into HTML if we updated the template or the post
        # since the last time we ran the script
        if (template_update > LAST_UPDATED or
            file_update > LAST_UPDATED):

            # Set file_path to be new file_path
            if new_file_path != None:
                file_path = new_file_path
            
            # Parse file
            with open(file_path, 'r+') as f:
                post_text = f.read()
                post_only = extractText(post_text)
                parsed_file = markdown(post_text, extras=['metadata'])
                title = parsed_file.metadata['title']

                # Remove the old HTML file if it exists:
                if str(post_id) in POSTS_DICT['POSTS'].keys() and not id_as_slug:    
                    anchor = POSTS_DICT['POSTS'][str(post_id)]['anchor']
                    old_file = OUTPUT_DIR + anchor +'.html'
                    os.remove(old_file)

                # Get provided summary or first 100 chars of .md file
                if 'summary' in parsed_file.metadata.keys():
                    summary = parsed_file.metadata['summary']
                else:
                    summary = post_only[0:100] + '…'
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
                env = Environment(loader=FileSystemLoader(TEMPLATE_DIR)) 
                post_html = env.get_template(POST_TEMPLATE).render(post = data, 
                    max_num = ID_COUNT)

                # Toggle between id or anchor as file name
                if id_as_slug:
                    post_name = str(post_id)
                else:
                    post_name = str(anchor)

                # Save new HTML file
                with open(OUTPUT_DIR + post_name+'.html', 'w') as output:
                    output.write(post_html)

            # Update message
            print("Updated: ", title)

    # Save new POSTS_DICT to metadata
    POSTS_DICT['ID_COUNT'] = ID_COUNT
    with open(METADATA_DIR + POSTS_DICT_FILE, 'w') as outfile:
        json.dump(POSTS_DICT, outfile, indent=4)

    # Update Posts Index with all posts

    # Sort descending date
    if (sort_date):
        POSTS_LIST = [POSTS_DICT["POSTS"][p] for p in sorted(
            POSTS_DICT["POSTS"], key=lambda x: POSTS_DICT["POSTS"][x]['last-updated'],
            reverse=True
        )]
    # Else, sort by descending ID
    else:
        POSTS_LIST = [POSTS_DICT["POSTS"][p] for p in sorted(
            POSTS_DICT["POSTS"], key=lambda x: int(POSTS_DICT["POSTS"][x]['id']),
            reverse=True
        )]

    env = Environment(loader=FileSystemLoader(TEMPLATE_DIR)) 
    index_html = env.get_template(INDEX_TEMPLATE).render(posts = POSTS_LIST)
    with open (OUTPUT_DIR + 'index.html', 'w') as output:
        output.write(index_html)



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