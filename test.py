import volta
import os
from urllib.parse import unquote

def iterate_folder(folder, f):
  for p in os.listdir(folder):
    file_path = os.path.join(folder, p)
    if os.path.isdir(file_path):
      continue
    f(file_path)

def clear_folder(folder):
  iterate_folder(folder, lambda p: os.remove(p))

def remove_num(folder):
  def rename(path):
    folder, base = os.path.split(path)
    new_path = folder + '/' + base[0:base.find('#')] + '.md'
    os.rename(path, new_path)
  iterate_folder(folder, rename)

def requote(folder):
  def rename(path):
    os.rename(path, unquote(path))
  iterate_folder(folder, rename)

requote('contents/')
requote('contents/muse/')
