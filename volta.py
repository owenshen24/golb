# TODO: 
'''
Add support for declaring new entries to parse in sub-folders
Figure out my templating and css
Re-build the site
'''

import os
import json
import sys
import time
import re
import argparse
from urllib.parse import quote
from datetime import datetime
from jinja2 import Environment, FileSystemLoader
from markdown2 import markdown



CONFIG_PATH = ".config.json"
CONFIG = {}



def check_config():
  try:
    with open(CONFIG_PATH, 'r') as infile:
      global CONFIG
      CONFIG = json.load(infile)
  except EnvironmentError:
    ans = input('.config.json not found. Create default .config.json? (Y/N)')
    if ans.lower() == 'y':
      title = input('Enter name of project: ')
      init_config(title)
      print('Created .config.json')
      return check_config()
    else:
      print('Exiting...')
      sys.exit(0)



def init_config(title):
  default_config = {
    "CONTENTS_DIR": "contents/",
    "METADATA_DIR": "metadata/",
    "OUTPUT_DIR": "output/",
    "PAGE_DIR": "page/",
    "TEMPLATES_DIR": "templates/",
    "BASE_PATH": "base.html",
    "POST_PATH": "post.html",
    "INDEX_PATH": "index.html",
    "PAGE_PATH": "page.html",
    "POST_INDEX": "POST_INDEX.json",
    "PAGE_INDEX": "PAGE_INDEX.json",
    "LAST_UPDATED": 0,
    "MAX_SUMMARY_LENGTH": 150,
    "TITLE": title
  }
  with open(".config.json", 'w') as outfile:
    json.dump(default_config, outfile, indent=4)



def get_paths():
  paths = {
    "POST": {
      "CONTENTS": CONFIG['CONTENTS_DIR'],
      "OUTPUT": CONFIG['OUTPUT_DIR'],
      "FILE_INDEX": os.path.join(CONFIG['METADATA_DIR'], CONFIG['POST_INDEX']),
      "TEMPLATE": os.path.join(CONFIG['TEMPLATES_DIR'], CONFIG['POST_PATH']),
      "parse": True
    },
    "PAGE": {
      "CONTENTS": os.path.join(CONFIG['CONTENTS_DIR'], CONFIG['PAGE_DIR']),
      "OUTPUT": os.path.join(CONFIG['OUTPUT_DIR'], CONFIG['PAGE_DIR']),
      "FILE_INDEX": os.path.join(CONFIG['METADATA_DIR'], CONFIG['PAGE_INDEX']),
      "TEMPLATE": os.path.join(CONFIG['TEMPLATES_DIR'], CONFIG['PAGE_PATH']),
      "parse": True
    },
    "INDEX": {
      "PATH": os.path.join(CONFIG['CONTENTS_DIR'], CONFIG['INDEX_PATH']),
      "OUTPUT": os.path.join(CONFIG['OUTPUT_DIR'], CONFIG['INDEX_PATH']),
      "FILE_INDEX": os.path.join(CONFIG['METADATA_DIR'], CONFIG['POST_INDEX']),
      "TEMPLATE": os.path.join(CONFIG['TEMPLATES_DIR'], CONFIG['INDEX_PATH']),
      "parse": False
    },
    "BASE": {
      "TEMPLATE": os.path.join(CONFIG['TEMPLATES_DIR'], CONFIG['BASE_PATH']),
      "parse": False
    }
  }
  return paths



def extract_text(text):
    _meta_data_newline = re.compile("^\n", re.MULTILINE)
    _meta_data_pattern = re.compile(r'^(?:---[\ \t]*\n)?(.*:\s+>\n\s+[\S\s]+?)(?=\n\w+\s*:\s*\w+\n|\Z)|([\S\w]+\s*:(?! >)[ \t]*.*\n?)(?:---[\ \t]*\n)?', re.MULTILINE)
    metadata_split = re.split(_meta_data_newline, text, maxsplit=1)
    metadata_content = metadata_split[0]
    match = re.findall(_meta_data_pattern, metadata_content)
    if not match:
        return text
    tail = metadata_split[1]
    return tail



def get_file_index(index_path):
  try:
    with open(index_path, 'r') as infile:
      FILE_INDEX = json.load(infile)
      return FILE_INDEX
  except EnvironmentError:
    print(index_path + ' not found, creating new ' + index_path)
    new_index = {}
    with open(index_path, 'w') as outfile:
      json.dump(new_index, outfile, indent=4)
    print('Created ' + index_path)
    return get_file_index(index_path)



def parse_posts(input_dir, output_dir, template_path, index_path, parse_all=False):
  FILE_INDEX = get_file_index(index_path)
  NOT_IN_FILE_INDEX = set([k for k in FILE_INDEX])
  for post in os.listdir(input_dir):
    file_path = os.path.join(input_dir, post)
    file_update = int(os.path.getmtime(file_path))
    post_id = str(os.stat(file_path).st_ino) + str(os.stat(file_path).st_dev)

    # Skip subdirectories:
    if os.path.isdir(file_path):
        continue
    if (parse_all or file_update > CONFIG["LAST_UPDATED"]):
      # Remove the old HTML file if it exists:
      try:
        os.remove(os.path.join(output_dir, FILE_INDEX[post_id]['anchor']))
      # Ignore if the file is new (index missing key), or if the output doesn't exist
      except (EnvironmentError, KeyError):
        pass
      # Begin parsing the file
      with open(file_path, 'r+') as f:
        p = f.read()
        post_body = extract_text(p)
        parsed_file = markdown(p, extras=['metadata', 'smarty-pants'])
        post_metadata = {
          'title': None,
          'anchor': None,
          'summary': None,
          'word_count': None,
          'date': datetime.fromtimestamp(
          file_update).strftime('%Y-%m-%d %H:%M'),
          'last_updated': file_update
        }

        # Add post attributes
        try:
          post_metadata['title'] = parsed_file.metadata['title']
        except KeyError:
          title = os.path.splitext(post)[0]
          post_metadata['title'] = quote(title.replace(' ', '-'))
        try:
          post_metadata['anchor'] = parsed_file.metadata['anchor']
        except KeyError:
          post_metadata['anchor'] = quote(post_metadata['title'].replace(' ', '-'))
        try:
          post_metadata['summary'] = parsed_file.metadata['summary']
        except KeyError:
          post_metadata['summary'] = post_body[0:CONFIG["MAX_SUMMARY_LENGTH"]] + '...'
        post_metadata['word_count'] = len(post_body.split(' '))
        
        # Add to FILE_INDEX (either overwriting or adding a new entry)
        FILE_INDEX[post_id] = post_metadata
        data = post_metadata.copy()
        data['content'] = parsed_file
        html_path = output_dir + data['anchor'] + '.html'

        # Create HTML file
        render_HTML(html_path, template_path, data)
        print("Updated: ", data['title'])

        # Keep track of what FILE_INDEX has
        # (KeyErrors are okay, as they merely mean the post_id is new)
        try:
          NOT_IN_FILE_INDEX.remove(post_id)
        except KeyError:
          pass
  
  # Remove obsolete keys and update FILE_INDEX
  for obsolete_key in NOT_IN_FILE_INDEX:
      FILE_INDEX.pop(obsolete_key)
  with open(index_path, 'w') as outfile:
    json.dump(FILE_INDEX, outfile, indent=4)



def render_HTML(output_path, template_path, data):
  env = Environment(loader=FileSystemLoader('./')) 
  post_html = env.get_template(template_path).render(data = data, title = CONFIG['TITLE'])
  with open(output_path, 'w') as outfile:
    outfile.write(post_html)



def need_to_update(template_path):
  # Either the specified template or the base template has been updated since last run
  return (int(os.path.getmtime(template_path)) > CONFIG["LAST_UPDATED"] or
    int(os.path.getmtime(get_paths()["BASE"]["TEMPLATE"])) > CONFIG["LAST_UPDATED"]
  )



def update(input_path, output_path, template_path, index_path):
  # Check if template has been updated
  if need_to_update(template_path):
    print(template_path + ' has been updated since last run. Updating all files in ' + input_path)
    for post in os.listdir(output_path):
        file_path = os.path.join(output_path, post)
        # Skip subdirectories:
        if os.path.isdir(file_path):
          continue
        if post != 'index.html':
          os.remove(file_path)
    parse_all = True
  else:
    parse_all = False
  # Rebuild either all posts or some posts
  parse_posts(input_path, output_path, template_path, index_path, parse_all=parse_all)



def update_contents():
  contents = get_paths()
  for k in contents.keys():
    c = contents[k]
    if c["parse"]:
      update(c["CONTENTS"], c["OUTPUT"], c["TEMPLATE"], c["FILE_INDEX"])



def update_index():
  c = get_paths()["INDEX"]
  # Check if index template has been updated
  if need_to_update(c["TEMPLATE"]):
    # Remove old index
    try: 
      os.remove(c["OUTPUT"])
    except FileNotFoundError:
      pass
    # Build the new index page
    FILE_INDEX = get_file_index(c["FILE_INDEX"])
    render_HTML(c["OUTPUT"], c["TEMPLATE"], FILE_INDEX)
    print('Updated index.html')



def update_time():
  CONFIG['LAST_UPDATED'] = time.time()
  with open(CONFIG_PATH, 'w') as infile:
      json.dump(CONFIG, infile, indent=4)



def build_site():
  update_contents()
  update_index()
  update_time()



if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument("-r", "--rebuild", help="Rebuilds the entire site", action="store_true")
  args = parser.parse_args()
  check_config()
  if args.rebuild:
    CONFIG["LAST_UPDATED"] = 0
  build_site()
