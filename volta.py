import os
import json
import time
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


def parsePosts():
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

        # Create new entry in POSTS_DICT and rename file if new
        # Otherwise, get existing post_id
        if '_' not in file_path:
            ID_COUNT += 1
            post_id = ID_COUNT
            new_file_path = file_path[:file_path.find('.md')] + '_' + str(ID_COUNT) + '.md'
            os.rename(file_path, new_file_path)
        else:
            post_id = int(post[post.find('_')+1:post.find('.md')])

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

                # Parse the HTML using Jinja and create the page
                env = Environment(loader=FileSystemLoader(TEMPLATE_DIR)) 
                post_html = env.get_template(POST_TEMPLATE).render(post = data)      
                with open(OUTPUT_DIR + str(anchor)+'.html', 'w') as output:
                    output.write(post_html)

            # Update message
            print("Updated: ", title)

    # Save new POSTS_DICT to metadata
    POSTS_DICT['ID_COUNT'] = ID_COUNT
    with open(METADATA_DIR + POSTS_DICT_FILE, 'w') as outfile:
        json.dump(POSTS_DICT, outfile, indent=4)

    # Update Posts Index with all posts
    env = Environment(loader=FileSystemLoader(TEMPLATE_DIR)) 
    index_html = env.get_template(INDEX_TEMPLATE).render(
    posts = POSTS_DICT['POSTS'].values())
    with open (OUTPUT_DIR + 'index.html', 'w') as output:
        output.write(index_html)


# If script is run:
if __name__ == "__main__":
    updateTime()
    loadConfig(OPTIONS[0])
    parsePosts()
    loadConfig(OPTIONS[1])
    #parsePosts()