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
from misaka import Markdown, HtmlRenderer



CONFIG_PATH = ".config.json"
CONFIG = {}
PATHS_PATH = ".paths.json"
PATHS = {}



def check_config():
  try:
    with open(CONFIG_PATH, 'r') as infile:
      global CONFIG
      CONFIG = json.load(infile)
  except EnvironmentError:
    ans = input('.config.json not found. Create default .config.json? (Y/N)')
    if ans.lower() == 'y':
      init_config()
      print('Created .config.json')
      return check_config()
    else:
      print('Exiting...')
      sys.exit(0)



def init_config():
  default_config = {
    "LAST_UPDATED": 0,
    "MAX_SUMMARY_LENGTH": 150
  }
  with open(".config.json", 'w') as outfile:
    json.dump(default_config, outfile, indent=4)



def load_paths():
  try:
    with open(PATHS_PATH, 'r') as infile:
      global PATHS
      PATHS = json.load(infile)
  except EnvironmentError:
    print(PATHS_PATH + ' not found')



# Returns metadata dict as well as text
def extract_text(text):
  metadata = {}
  _key_val_pat = re.compile(r"[\S\w]+\s*:(?! >)[ \t]*.*\n?", re.MULTILINE)
  _key_val_block_pat = re.compile(
        "(.*:\s+>\n\s+[\S\s]+?)(?=\n\w+\s*:\s*\w+\n|\Z)", re.MULTILINE)
  _meta_data_newline = re.compile("^\n", re.MULTILINE)
  _meta_data_pattern = re.compile(r'^(?:---[\ \t]*\n)?(.*:\s+>\n\s+[\S\s]+?)(?=\n\w+\s*:\s*\w+\n|\Z)|([\S\w]+\s*:(?! >)[ \t]*.*\n?)(?:---[\ \t]*\n)?', re.MULTILINE)
  metadata_split = re.split(_meta_data_newline, text, maxsplit=1)
  metadata_content = metadata_split[0]
  match = re.findall(_meta_data_pattern, metadata_content)
  if not match:
      return text
  tail = metadata_split[1]
  kv = re.findall(_key_val_pat, metadata_content)
  kvm = re.findall(_key_val_block_pat, metadata_content)
  kvm = [item.replace(": >\n", ":", 1) for item in kvm]
  for item in kv + kvm:
    k, v = item.split(":", 1)
    metadata[k.strip()] = v.strip()
  return metadata, tail



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
  updated_index = False
  NOT_IN_INDEX = set([s for s in FILE_INDEX.keys()])
  for post in os.listdir(input_dir):
    file_path = os.path.join(input_dir, post)
    file_update = int(os.path.getmtime(file_path))
    post_id = str(os.stat(file_path).st_ino) + str(os.stat(file_path).st_dev)
    
    # Skip subdirectories:
    if os.path.isdir(file_path):
        continue
    
    # Remove to keep track of new files
    try:
      NOT_IN_INDEX.remove(post_id)
    except KeyError:
      pass

    # If we have to parse everything, or the file is an updated one
    if (parse_all or file_update > CONFIG["LAST_UPDATED"]):
      updated_index = True

      # Remove the old HTML file if it exists:
      try:
        os.remove(os.path.join(output_dir, FILE_INDEX[post_id]['anchor']))
      # Ignore if the file is new (index missing key), or if the output doesn't exist
      except (EnvironmentError, KeyError):
        pass
      # Begin parsing the file
      with open(file_path, 'r+') as f:
        p = f.read()
        parsed_metadata, post_body = extract_text(p)
        r = HtmlRenderer()
        md = Markdown(r, extensions=('fenced-code','math', 'math-explicit'))
        parsed_file = md(post_body)
        post_metadata = {
          'title': '',
          'anchor': None,
          'summary': None,
          'word_count': None,
          'date': datetime.fromtimestamp(
          file_update).strftime('%Y-%m-%d %H:%M'),
          'last_updated': file_update
        }

        # Add post attributes
        try:
          post_metadata['title'] = parsed_metadata['title']
        except KeyError:
          post_metadata['title'] = os.path.splitext(post)[0]
        
        try:
          post_metadata['anchor'] = parsed_metadata['anchor']
        except KeyError:
          post_metadata['anchor'] = post_id
        
        try:
          post_metadata['summary'] = parsed_metadata['summary']
        except KeyError:
          post_metadata['summary'] = post_body[0:CONFIG["MAX_SUMMARY_LENGTH"]] + '...'
        
        post_metadata['word_count'] = len(post_body.split(' '))
        
        # Add to FILE_INDEX (either overwriting or adding a new entry)
        FILE_INDEX[post_id] = post_metadata
        data = post_metadata.copy()
        data['content'] = parsed_file
        html_path = os.path.join(output_dir, (post_metadata['anchor'] + '.html'))

        # Create HTML file
        render_HTML(html_path, template_path, data)
        print("Updated: ", data['title'])
        
        # Rename file
        new_title = post_metadata['title'].replace(' ', '-')
        new_file_path = os.path.join(input_dir, (new_title + '.md'))
        os.rename(file_path, new_file_path)

  # Update FILE_INDEX
  # Remove obsolete posts
  for k in NOT_IN_INDEX:
    try:
      os.remove(os.path.join(output_dir, (FILE_INDEX[k]['anchor'] + '.html')))
      updated_index = True
    except EnvironmentError:
      pass
  if updated_index:
    with open(index_path, 'w') as outfile:
      json.dump(FILE_INDEX, outfile, indent=4)



def render_HTML(output_path, template_path, data):
  env = Environment(loader=FileSystemLoader('./')) 
  post_html = env.get_template(template_path).render(data = data)
  with open(output_path, 'w') as outfile:
    outfile.write(post_html)



def need_to_update_template(template_path):
  # Either the specified template or the base template has been updated since last run
  return (int(os.path.getmtime(template_path)) > CONFIG["LAST_UPDATED"] or
    int(os.path.getmtime(PATHS["BASE"]["TEMPLATE"])) > CONFIG["LAST_UPDATED"]
  )



def need_to_update_index(index_path):
  return (int(os.path.getmtime(index_path)) > CONFIG["LAST_UPDATED"])



def update(input_path, output_path, template_path, index_path):
  # Check if template has been updated
  if need_to_update_template(template_path):
    print(template_path + ' has been updated since last run. Updating all files in ' + input_path)
    for post in os.listdir(output_path):
        file_path = os.path.join(output_path, post)
        
        # Skip subdirectories and index:
        if os.path.isdir(file_path):
          continue
        if post != 'index.html':
          os.remove(file_path)
    parse_all = True
  else:
    parse_all = False
  # Rebuild either all posts or some posts
  parse_posts(input_path, output_path, template_path, index_path, parse_all=parse_all)



def update_index(file_index_path, output_path, template_path):
  # Check if index template has been updated or we added new posts
  if need_to_update_template(template_path) or need_to_update_index(file_index_path):
    # Remove old index
    try: 
      os.remove(output_path)
    except FileNotFoundError:
      pass
    # Build the new index page
    FILE_INDEX = get_file_index(file_index_path)
    render_HTML(output_path, template_path, FILE_INDEX)
    print('Updated: ' + output_path)



def update_contents():
  # Do all post-types first because they'll update their corresponding
  # FILE_INDEX files before updating the indexes
  for k in PATHS.keys():
    c = PATHS[k]
    if c["TYPE"] == "post":
      update(c["CONTENTS"], c["OUTPUT"], c["TEMPLATE"], c["FILE_INDEX"])
  for k in PATHS.keys():
    c =PATHS[k]
    if c["TYPE"] == "index":
      update_index(c["FILE_INDEX"], c["OUTPUT"], c["TEMPLATE"])



def update_time():
  CONFIG['LAST_UPDATED'] = time.time()
  with open(CONFIG_PATH, 'w') as infile:
      json.dump(CONFIG, infile, indent=4)



def build_site():
  update_contents()
  update_time()



if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument("-r", "--rebuild", help="Rebuilds the entire site", action="store_true")
  args = parser.parse_args()
  check_config()
  load_paths()
  if args.rebuild:
    CONFIG["LAST_UPDATED"] = 0
    # Remove all old indices
    for k in PATHS.keys():
      p = PATHS[k]
      if p["TYPE"] == "index":
        try:
          os.remove(p["FILE_INDEX"])
        except Exception as e:
          pass
  build_site()
