#!/usr/bin/python
import sys, tty, termios, subprocess, os, json, glob

DIR_PATH = os.path.expanduser("~/Dropbox/tbrush_notes")

def getch():
  # Return a single character from stdin.

  fd = sys.stdin.fileno()
  old_settings = termios.tcgetattr(fd)
  try:
    tty.setraw(sys.stdin.fileno())
    ch = sys.stdin.read(1)
  finally:
    termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
  return ch

def main_loop():
  # Wait for a key, build up the query string.

  notes = Notes()
  query_string = ''
  while True:
    print '-- query: {} --'.format(query_string)

    ch = getch()
    if ord(ch) == 3:  # ctrl+c
      raise KeyboardInterrupt
    elif ord(ch) == 127:  # backspace
      query_string = query_string[:-1]
    elif ord(ch) == 13:  # return
      if len(notes.matched_basenames) == 0:
        notes.new_note(query_string)
      notes.open_all()
      break
    else:
      query_string += ch
    notes.search(query_string)

class Notes:
  def __init__(self):
    self.dir_path = os.path.expanduser(DIR_PATH)
    self.meta_path = os.path.expanduser('~/.toothbrush')
    self.basename_to_content = {}
    glob_path = os.path.join(self.dir_path, '*.txt')
    for path in glob.glob(glob_path):
      basename = os.path.splitext(os.path.basename(path))[0]
      with open(path) as f:
        self.basename_to_content[basename] = f.read()

    self.basename_to_open_count = {}
    if os.path.exists(self.meta_path):
      with open(self.meta_path) as f:
        text = f.read()
      try:
        self.basename_to_open_count = json.loads(text)
      except Exception:
        pass

  def search(self, query_string):
    self.matched_basenames = []

    terms = set(query_string.split())
    for basename, content in self.basename_to_content.iteritems():
      for term in terms:
        if term not in basename and term not in content:
          break
      else:
        self.matched_basenames.append(basename)

    self.matched_basenames.sort(key=lambda basename: self.basename_to_open_count.get(basename, 0))

    for basename in self.matched_basenames[:10]:
      print basename

    if not self.matched_basenames:
      print '~ nothing found ~'

  def open_all(self):
    for basename in self.matched_basenames[:10]:
      path = os.path.join(self.dir_path, basename)
      self.open_path(path)

  def open_path(self, path):
    print 'opening:', path

    basename = os.path.basename(path)
    self.basename_to_open_count.setdefault(basename, 0)
    self.basename_to_open_count[basename] += 1
    with open(self.meta_path, 'w') as f:
      f.write(json.dumps(self.basename_to_open_count))

    os.system('open "{}"'.format(path))

  def new_note(self, query_string):
    new_path = os.path.join(DIR_PATH, query_string) + '.txt'
    with open(new_path, 'w') as f:
      f.write('')
    self.open_path(new_path)

if __name__ == '__main__':
  main_loop()
