#!/usr/bin/python3

# Prints the daily verse from https://dailyverses.net
# TODO: Also parse random verse page: https://dailyverses.net/random-bible-verse

try:
    import requests
except Exception:
    print("Please install the dependencies with:")
    print("  python3 -m pip install -r requirements.txt")
    exit(1)


LANG       = "esv"    # esv, kjv, niv, nkjv, nlt, nrsv
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36"
URL        = "https://dailyverses.net/get/verse.js?language=" + LANG

def parse_verse(txt):
    # Lisp for life
    cdr    = txt.split("\\u003e")[1]
    car    = cdr.split("\\u003c")[0]
    result = car.replace("\u2014", " -")
    return result.encode().decode("unicode-escape")

def main():
    r = requests.get(URL,
                     allow_redirects = True,
                     headers = { 'User-Agent': USER_AGENT })

    verse = parse_verse(r.text)
    print(verse)

main()
