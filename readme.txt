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

If you have trouble getting pip set up you can just remove the two lines that include the string
"clipboard" in the main python file and skip the `pip install` step. (It's not very important.)

Usage
---

Run the script:
`t`

Just start typing to search your notes.
Press the up/down arrows to select a note.
Hit return to either open the matching file or create a new file if there are no matches.

ctrl+n will also create a new note from the current query

License
---
MIT
