#!/usr/bin/python3

try:
    import sys, requests, bs4
except Exception:
    print("Please install the dependencies with:")
    print("  python3 -m pip install -r requirements.txt")
    exit(1)

##########################
DEBUG       = False      # Print extra information.
RECURSE     = True       # Will go to the next chapter until finished
LINE_LIMIT  = 85         # Will jump to the next line if too long. 0 means disabled.
LINE_INDENT = 6          # Start of text lines.
NUM_PAD     = 5          # Padding for the numbers.
VERSION     = "dhh"      # Bible version.
FIRST_BOOK  = "genesis"  # Only used for replacing START_URL
FIRST_CHAP  = "1"        #
##########################

BASE_URL  = "https://www.biblia.es/"
START_URL = BASE_URL + f"biblia-buscar-libros-1.php?libro={FIRST_BOOK}&capitulo={FIRST_CHAP}&version={VERSION}"

# For similar C version with comments, see 8dcc/text-formatter
# String is the string to print, limit is the max position in a line, cur_indent is
# the current indentation of the text to be printed.
def print_limited(string, limit, cur_indent):
    if (string == None):
        if (DEBUG):
            sys.stderr.write("print_limited: Got None string")
        return

    # For printing the last word. Space and not newline because we also want to check
    # if the last word is on the line limit.
    string += ' '

    line_p     = 0
    last_space = ''
    last_word  = ""
    for c in string:
        if (c == ' '):
            if line_p <= limit - cur_indent:
                if (last_space != ''):
                    sys.stdout.write(last_space)

                if (last_space == '\n'):
                    line_p = cur_indent + len(last_word)
            else:
                if (last_space != ''):
                    sys.stdout.write('\n')

                    # Indent line
                    for i in range(cur_indent):
                        sys.stdout.write(' ')

                line_p = cur_indent + len(last_word)

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
        # Extra spaces so line is clean when returning
        if (DEBUG):
            print("Getting: " + url + "                   \r")

        r = requests.get(url,
                         allow_redirects=True,
                         headers = {
                             'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36'
                             }
                         )

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
                sys.stdout.write('\n========================================\n')
                print(item.string.upper().center(40))
                sys.stdout.write('========================================\n\n')
            elif (item.get("class")[0] == "estudio"):
                if (last_printed != "capitulo"):
                    sys.stdout.write('\n')
                print(item.string)
                sys.stdout.write('\n')
            elif (item.get("class")[0] == "versiculo"):
                sys.stdout.write(item.string.rjust(NUM_PAD))
                for i in range(LINE_INDENT - NUM_PAD):
                    sys.stdout.write(' ')
            elif (item.get("class")[0] == "texto"):
                # In theory we just printed the number
                for s in item.strings:
                    final_str = str(s).replace(chr(0x2014), "- ").replace("\r\n", "")

                    if (last_printed == "texto"):
                        final_str = "".rjust(LINE_INDENT) + final_str

                    if (LINE_LIMIT == 0):
                        # No line limit, just print
                        print(final_str)
                    else:
                        # Line limit, jump to the next line if the line is too long
                        print_limited(final_str, LINE_LIMIT, LINE_INDENT)

                    last_printed = "texto"
            elif (DEBUG):
                sys.stdout.write(item.name)
                sys.stdout.write('\t')
                sys.stdout.write(item.get("class")[0])
                sys.stdout.write('\t')
                sys.stdout.write(item.string)
                sys.stdout.write('\n')

            last_printed = item.get("class")[0]

main()

