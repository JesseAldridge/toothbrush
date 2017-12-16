Installation
---

Something like this:
```
git clone git@github.com:JesseAldridge/toothbrush.git
cd toothbrush
pip install -r requirements.txt
ln -s /Users/jesse_aldridge/Dropbox/toothbrush/toothbrush.py /usr/local/bin/t
```

Set DIR_PATH at the top of toothbrush.py to the directory that you will use to store your notes.

Usage
---

Run the script:
`t`

Just start typing to search your notes.
Press the up/down arrows to select a note.
Hit return to either open the matching file or create a new file if there are no matches.

ctrl+a to copy the content of the selected note to the clipboard
ctrl+n to create a new note from the current query

License
---
MIT
