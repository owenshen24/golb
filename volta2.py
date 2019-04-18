import os
import json
import time
from datetime import datetime
from jinja2 import Environment, FileSystemLoader
from markdown2 import markdown

# Path variables
CONFIG_PATH = "metadata/config.json"
OPTIONS = [
    "posts",
    "muse"
]


def loadConfig(options):
    with open(CONFIG_PATH, 'r') as infile:
        CONFIG = json.load(infile)[options]
        return CONFIG


def parsePosts(CONFIG):
    # Define path variables
    CONTENTS_DIR = CONFIG['CONTENTS_DIR']
    METADATA_DIR = CONFIG['METADATA_DIR']
    POSTS_DICT_FILE = CONFIG['METADATA_DICT']
    OUTPUT_DIR = CONFIG['OUTPUT_DIR']
    POST_TEMPLATE = CONFIG["POST_TEMPLATE_PATH"]
    INDEX_TEMPLATE = CONFIG["INDEX_TEMPLATE_PATH"]

    # Load up the POSTS_DICT
    POSTS_DICT = {}
    with open(METADATA_DIR + POSTS_DICT_FILE, 'r') as infile:
        POSTS_DICT = json.load(infile)
        ID_COUNT = POSTS_DICT['ID_COUNT']

    # Get last updated time for template
    # template_update1 = int(os.path.getmtime(POST_TEMPLATE))
    # template_update2 = int(os.path.getmtime(INDEX_TEMPLATE))

    # Iterate through all posts
    for post in os.listdir(CONTENTS_DIR):
        file_path = os.path.join(CONTENTS_DIR, post)
        file_update = int(os.path.getmtime(file_path))
        post_id = None
        new_file_path = None

        # Create new entry in POSTS_DICT and rename file if new
        # Otherwise, get existing post_id
        if '_' not in file_path:
            ID_COUNT += 1
            post_id = ID_COUNT
            new_file_path = file_path[:file_path.find('.md')] + '_' + str(ID_COUNT) + '.md'
            os.rename(file_path, new_file_path)
        else:
            post_id = int(post[post.find('_')+1:post.find('.md')])

        # Update the HTML file if anything updated since we last wrote the file
        # TODO: Hard to check all the possible ways this could happen, and this
        # doesn't need to scale. So don't worry about it for now.
        '''
        template_update1 > file_update 
        or template_update2 > file_update
        or str(post_id) not in POSTS_DICT['POSTS'].keys()
        or file_update > POSTS_DICT['POSTS'][str(post_id)]['last-updated']
        '''
        if (True):

            # Set file_path to be new file_path
            if new_file_path != None:
                file_path = new_file_path
            
            # Parse file
            with open(file_path, 'r+') as f:
                post_text = f.read()
                parsed_file = markdown(post_text, extras=['metadata'])
                title = parsed_file.metadata['title']
                summary = parsed_file.metadata['summary']
                anchor = title.replace(' ', '-')
                word_count = len(post_text.split(' '))
                data = {
                    'title': title,
                    'date': datetime.fromtimestamp(
                    file_update).strftime('%Y-%m-%d %H:%M'),
                    'last-updated': file_update,
                    'anchor': anchor,
                    'summary': summary,
                    'word_count': word_count
                }
                POSTS_DICT['POSTS'][str(post_id)] = data.copy()

                # Add content to data dict
                data['content'] = parsed_file
                data['summary'] = summary


if __name__ == "__main__":
    CONFIG = loadConfig(OPTIONS[0])
    parsePosts(CONFIG)
