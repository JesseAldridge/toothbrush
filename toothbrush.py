#!/usr/bin/python
import sys, tty, termios, subprocess, os, json, glob, time

DIR_PATH_NOTES = os.path.expanduser("~/Dropbox/tbrush_notes")
DIR_PATH_META = os.path.expanduser('~/.toothbrush_meta')

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

  if not os.path.exists(DIR_PATH_META):
    os.mkdir(DIR_PATH_META)

  start_time = time.time()
  notes = Notes()
  query_string = ' '.join(sys.argv[1:])
  query_path = os.path.join(DIR_PATH_META, 'saved_query.txt')
  if not query_string.strip() and os.path.exists(query_path):
    with open(query_path) as f:
      query_string = f.read()
  load_times_path = os.path.join(DIR_PATH_META, 'load_times.txt')
  print 'load_times_path:', load_times_path
  with open(load_times_path, 'a') as f:
    f.write('{}\n'.format(time.time() - start_time))

  first_char_typed = False
  while True:
    print '\nquery: {}\n'.format(query_string)

    notes.search(query_string)
    ch = getch()

    if ord(ch) == 3:  # ctrl+c
      raise KeyboardInterrupt
    elif ord(ch) == 14:  # ctrl+n
      notes.new_note(query_string)
    elif ord(ch) == 23:  # ctrl+w
      query_string = query_string.rsplit(' ', 1)[0] if ' ' in query_string else ''
    elif ord(ch) == 127:  # backspace
      query_string = query_string[:-1]
    elif ord(ch) == 13:  # return
      if len(notes.matched_basenames) == 0:
        notes.new_note(query_string)
      else:
        notes.open_selected()
      break
    elif ord(ch) == 27:  # esc code
      ch = getch() # skip the [
      ch = getch()
      if ord(ch) == 66 or ord(ch) == 65: # up/down arrows
        notes.adjust_selection(1 if ord(ch) == 66 else -1)
    else:
      if not first_char_typed:
        query_string = ''
        first_char_typed = True
      query_string += ch

    with open(query_path, 'w') as f:
      f.write(query_string)

class Notes:
  def __init__(self):
    self.dir_path = os.path.expanduser(DIR_PATH_NOTES)
    self.selected_index = None
    self.basename_to_content = {}
    self.basename_to_content_lower = {}
    self.matched_basenames = []
    glob_path = os.path.join(self.dir_path, '*.txt')
    for path in glob.glob(glob_path):
      basename = os.path.splitext(os.path.basename(path))[0]
      with open(path) as f:
        self.basename_to_content[basename] = f.read()
      self.basename_to_content_lower[basename] = self.basename_to_content[basename].lower()

  def search(self, query_string):
    self.matched_basenames = []
    self.query_string = query_string

    terms = set(query_string.lower().split())
    for basename, content in self.basename_to_content_lower.iteritems():
      for term in terms:
        if term not in basename and term not in content:
          break
      else:
        self.matched_basenames.append(basename)

    self.matched_basenames.sort(key=self.score, reverse=True)
    num_matches_to_show = 10

    for i, basename in enumerate(self.matched_basenames[:num_matches_to_show]):
      print '{}{}'.format('> ' if i == self.selected_index else '  ', basename)
      if i == self.selected_index:
        full_text = self.basename_to_content[basename].strip()
        lines = full_text.splitlines()
        indented_lines = ['     ' + line for line in lines]
        content_preview = '\n'.join(indented_lines)
        print content_preview

    if not self.matched_basenames:
      print '~ nothing found ~'
    elif len(self.matched_basenames) > num_matches_to_show:
      print '  ...'

  def score(self, basename):
    return 10 if self.query_string == basename else 0

  def open_selected(self):
    if self.selected_index is None:
      for i in range(len(self.matched_basenames)):
        self.open_index(i)
      return
    self.open_index(self.selected_index)

  def open_index(self, index):
    basename = self.matched_basenames[:10][index]
    path = os.path.join(self.dir_path, basename) + '.txt'
    self.open_path(path)

  def open_path(self, path):
    print 'opening:'
    print '"{}"'.format(path)
    os.system('open "{}"'.format(path))

  def new_note(self, query_string):
    new_path = os.path.join(DIR_PATH_NOTES, query_string) + '.txt'
    with open(new_path, 'w') as f:
      f.write('')
    self.open_path(new_path)

  def adjust_selection(self, amount):
    if not self.matched_basenames:
      self.selected_index = None
      return

    if self.selected_index is None:
      self.selected_index = 0
    else:
      self.selected_index += amount
    self.selected_index %= min(len(self.matched_basenames), 10)

if __name__ == '__main__':
  main_loop()
