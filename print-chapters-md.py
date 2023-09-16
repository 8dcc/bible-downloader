#!/usr/bin/python3

try:
    import sys, requests, bs4
except Exception:
    print("Please install the dependencies with:")
    print("  python3 -m pip install -r requirements.txt")
    exit(1)

##########################
RECURSE      = True       # Will go to the next chapter until finished
UPPER_TITLES = False      # Chapter titles in uppercase
LINE_LIMIT   = 0          # Will jump to the next line if too long. 0 means disabled.
VERSION      = "dhh"      # Bible version.
FIRST_BOOK   = "genesis"  # Only used for replacing START_URL
FIRST_CHAP   = "1"        #
##########################

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36"
BASE_URL   = "https://www.biblia.es/"
START_URL  = BASE_URL + f"biblia-buscar-libros-1.php?libro={FIRST_BOOK}&capitulo={FIRST_CHAP}&version={VERSION}"

# For similar C version with comments, see 8dcc/text-formatter
# String is the string to print, limit is the max position in a line
def print_limited(string, limit):
    if (string == None):
        return

    # For printing the last word. Space and not newline because we also want to
    # check if the last word is on the line limit.
    string += ' '

    line_p     = 0
    last_space = ''
    last_word  = ""
    for c in string:
        if (c == ' '):
            if line_p <= limit:
                if (last_space != ''):
                    sys.stdout.write(last_space)

                if (last_space == '\n'):
                    line_p = len(last_word)
            else:
                if (last_space != ''):
                    sys.stdout.write('\n')

                line_p = len(last_word)

            # Print last word and clear buf
            sys.stdout.write(last_word)
            last_word = ""

            last_space = c      # ' '
        elif (c == '\n'):
            sys.stdout.write(last_space)
            line_p = 0

            sys.stdout.write(last_word)
            last_word = ""

            last_space = c      # '\n'
        else:
            last_word += c

        line_p += 1

    sys.stdout.write('\n')

def main():
    url = START_URL
    while (url != ""):
        r = requests.get(url,
                         allow_redirects = True,
                         headers = { 'User-Agent': USER_AGENT })

        global_soup = bs4.BeautifulSoup(r.text, 'html.parser')
        contents = global_soup.find_all("div", {"class": "col_i_1_int_1"})

        # Nav buttons, used to get next chapter
        url = ""
        if (RECURSE):
            for item in contents[0].find_all("a"):
                if (item.string == "Capitulo siguiente"):
                    url = BASE_URL + item.get("href")
                    break

        # Used to check if we should print newline on certain combinations
        last_printed = ""

        for item in contents[1].find_all(["h3", "h2", "span"]):
            if (item.get("class") == None):
                continue

            if (item.get("class")[0] == "capitulo"):
                sys.stdout.write("### ")
                
                if (UPPER_TITLES):
                    print(item.string.upper())
                else:
                    print(item.string)
            elif (item.get("class")[0] == "estudio"):
                sys.stdout.write('\n')
                print("**" + item.string + "**")
                sys.stdout.write('\n')
            elif (item.get("class")[0] == "versiculo"):
                sys.stdout.write("<sup>")
                sys.stdout.write(item.string)
                sys.stdout.write("</sup> ")
            elif (item.get("class")[0] == "texto"):
                # In theory we just printed the number
                for s in item.strings:
                    final_str = str(s).replace(chr(0x2014), "- ").replace("\r\n", "")

                    # Line limit only makes it visual
                    if (LINE_LIMIT == 0):
                        # No line limit, just print
                        print(final_str)
                    else:
                        # Line limit, jump to the next line if the line is too long
                        print_limited(final_str, LINE_LIMIT)

                    sys.stdout.write('\n')      # 2nd newline for markdown
                    last_printed = "texto"

            last_printed = item.get("class")[0]

main()

