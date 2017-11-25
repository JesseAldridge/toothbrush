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
    sys.stdout.flush()
    print '-- query: {} --'.format(query_string)

    ch = getch()
    if ord(ch) == 3:  # ctrl+c
      raise KeyboardInterrupt
    elif ord(ch) == 127:  # backspace
      query_string = query_string[:-1]
    elif ord(ch) == 13:  # return
      if len(notes.selected_basenames) == 0:
        notes.new_note(query_string)

      for match_score, basename in notes.selected_basenames:
        notes.open(basename)
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
    for file_path in glob.glob(glob_path):
      filename = os.path.basename(file_path)
      basename = os.path.splitext(filename)[0]
      with open(file_path) as f:
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
    ranked_basenames = []
    terms = set(query_string.split())
    for basename, content in self.basename_to_content.iteritems():
      score = self.score(basename, content, terms)
      ranked_basenames.append((score, basename))
    ranked_basenames.sort(key=lambda t: -t[0])

    self.selected_basenames = []
    for i in range(0, min(len(ranked_basenames), 10)):
      score, basename = ranked_basenames[i]
      if i > 0:
        prev_score, prev_basename = ranked_basenames[i - 1]
        if score < prev_score * .5:
          break
      self.selected_basenames.append((score, basename))

    for score, basename in self.selected_basenames:
        print '{:<80} ({})'.format(basename[:80], round(score, 2))
    if not self.selected_basenames:
      print '~ nothing found ~'

  def score(self, basename, content, query_terms):
    basename_terms = set(basename.split())

    if basename_terms == query_terms:
      return 10

    score = 0
    for term in query_terms:
      if term in basename:
        score += 1
      if term in content:
        score += .5
      if term not in basename and term not in content:
        score -= 1
      score += self.basename_to_open_count.get(basename, 0) * .01
    return score

  def open(self, basename):
    print 'opening:', basename

    path = os.path.join(self.dir_path, basename) + '.txt'
    self.basename_to_open_count.setdefault(basename, 0)
    self.basename_to_open_count[basename] += 1
    with open(self.meta_path, 'w') as f:
      f.write(json.dumps(self.basename_to_open_count))

    os.system('open "{}"'.format(path))

  def new_note(self, query_string):
    new_path = os.path.join(DIR_PATH, query_string) + '.txt'
    with open(new_path, 'w') as f:
      f.write('')
    self.open(new_path)

if __name__ == '__main__':
  main_loop()
