# Bible downloader
**Downloads the bible in text format from [biblia.es](https://www.biblia.es/dios-habla-hoy.php)**

### Using
```console
$ git clone https://github.com/8dcc/bible-downloader
$ cd bible-downloader
$ python3 -m pip install -r requirements.txt
...
$ python3 print-chapters.py
...
```
That will print it to `stdout`, you can save it to a file using:
```console
$ python3 print-chapters.py > file.txt

$ python3 print-chapters.py | tee file.txt    # Also print
...
```

### Format
The format is pretty simple and it can be easily changed by editing the [constants](https://github.com/8dcc/bible-downloader/blob/b82a8cb8c45a9852618a153e0a3fcfd72af96817/print-chapters.py#L10-L19) in the code. Default format (although it would be easy to convert it to something like markdown):
```

========================================
                CHAPTER
========================================

Subtitle

    1 Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod
      tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam,
      quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo
      consequat.
    2 Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu
      fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident.
    3 Sunt in culpa qui officia deserunt mollit anim id est laborum.
    4 Molestie at elementum eu facilisis sed odio morbi quis commodo. Ornare
      suspendisse sed nisi lacus sed viverra. Ornare suspendisse sed nisi lacus sed
      viverra tellus in. Dui ut ornare lectus sit. Massa tincidunt dui ut ornare.
      
Subtitle 2

    5 Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod
      tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam,
      quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo
      consequat.

```

Note that lines can be intended and limited in length.
