Installation
---

Something like this:
```
git clone git@github.com:JesseAldridge/toothbrush.git
cd toothbrush
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

ctrl+n will also create a new note from the current query

Notes
---

This script works well for up to a few thousand notes. Beyond that the time it takes to read all
the files from the hard-drive can start to get annoying.
If you want something that works well with a high volume of notes, try:
https://github.com/JesseAldridge/electric_toothbrush


License
---
MIT
