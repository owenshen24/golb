import os
import json
import time
from datetime import datetime
from jinja2 import Environment, FileSystemLoader
from markdown2 import markdown

# Define path variables
CONTENTS_DIR = 'contents/'
METADATA_DIR = 'metadata/'
POSTS_DICT_FILE = 'POSTS_DICT.json'
OUTPUT_DIR = 'output/'
TEMPLATE_DIR = 'templates/'

# Load up the POSTS_DICT
POSTS_DICT = {}
with open(METADATA_DIR + POSTS_DICT_FILE, 'r') as infile:
  POSTS_DICT = json.load(infile)
ID_COUNT = POSTS_DICT['ID_COUNT']

# Get last updated time for template
template_update1 = int(os.path.getmtime(TEMPLATE_DIR + 'post.html'))
template_update2 = int(os.path.getmtime(TEMPLATE_DIR + 'index-template.html'))

# Iterate through all posts
for post in os.listdir(CONTENTS_DIR):
  file_path = os.path.join(CONTENTS_DIR, post)
  file_update = int(os.path.getmtime(file_path))
  
  post_id = None
  new_file_path = None

  # Create new entry in POSTS_DICT
  # Rename markdown file
  if '_' not in file_path:
    ID_COUNT += 1
    post_id = ID_COUNT
    new_file_path = file_path[:file_path.find('.md')] + '_' + str(ID_COUNT) + '.md'
    os.rename(file_path, new_file_path) 
  else:
    post_id = int(post[post.find('_')+1:post.find('.md')])
 
  # Update/Create the HTML file
  if (template_update1 > file_update 
      or template_update2 > file_update
      or post_id not in POSTS_DICT['POSTS'].keys()
      or file_update > POSTS_DICT['POSTS'][str(post_id)]['last-updated']):
    
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
      env = Environment(loader=FileSystemLoader('templates')) 
      post_html = env.get_template('post.html').render(post = data)      
      with open(OUTPUT_DIR + str(anchor)+'.html', 'w') as output:
        output.write(post_html)

# Save new POSTS_DICT to metadata
POSTS_DICT['ID_COUNT'] = ID_COUNT
with open(METADATA_DIR + POSTS_DICT_FILE, 'w') as outfile:
  json.dump(POSTS_DICT, outfile)

# Update Posts Index with all posts
env = Environment(loader=FileSystemLoader('templates')) 

index_html = env.get_template('index-template.html').render(
  posts = POSTS_DICT['POSTS'].values())
with open (OUTPUT_DIR + 'index.html', 'w') as output:
	output.write(index_html)