#!/usr/bin/python3

try:
    import sys, requests, bs4
except Exception:
    print("Please install the dependencies with:")
    print("  python3 -m pip install -r requirements.txt")
    exit(1)

DEBUG       = False      # Print extra information.
LINE_LIMIT  = 80          # Will jump to the next line if too long. 0 means disabled.
LINE_INDENT = 5          # Start of text lines.
NUM_PAD     = 4          # Padding for the numbers.
VERSION     = "dhh"      # Bible version.
BASE_URL    = f"https://www.biblia.es/biblia-buscar-libros-1.php?libro=BOOKNAME&capitulo=CHAPTERNUM&version={VERSION}"

# For similar C version with comments, see 8dcc/text-formatter
# String is the string to print, limit is the max position in a line, cur_indent is
# the current indentation of the text to be printed.
def print_limited(string, limit, cur_indent):
    # For printing the last word. Space and not newline because we also want to check
    # if the last word is on the line limit.
    if (string != ""):
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
    cur_book = "levitico"
    cur_chap = "1"
    url = BASE_URL.replace("BOOKNAME", cur_book)
    url = url.replace("CHAPTERNUM", cur_chap)

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
    content = contents[1]
    #print(content.prettify())

    for item in content.find_all(["h3", "h2", "span"]):
        if (item.get("class") == None):
            continue

        if (item.get("class")[0] == "capitulo"):
            sys.stdout.write('\n========================================\n')
            print(item.string.upper().center(40))
            sys.stdout.write('========================================\n')
        elif (item.get("class")[0] == "estudio"):
            sys.stdout.write('\n')
            print(item.string)
            sys.stdout.write('\n')
        elif (item.get("class")[0] == "versiculo"):
            sys.stdout.write(item.string.rjust(NUM_PAD))
            for i in range(LINE_INDENT - NUM_PAD):
                sys.stdout.write(' ')
        elif (item.get("class")[0] == "texto"):
            # In theory we just printed the number
            if (LINE_LIMIT == 0):
                # No line limit, just print
                print(item.string)
            else:
                # Line limit, jump to the next line if the line is too long
                print_limited(item.string, LINE_LIMIT, 5)

        elif (DEBUG):
            sys.stdout.write(item.name)
            sys.stdout.write('\t')
            sys.stdout.write(item.get("class")[0])
            sys.stdout.write('\t')
            sys.stdout.write(item.string)
            sys.stdout.write('\n')

    """
<div class="col_i_1_int_1">
 <h3 class="capitulo">
  Levítico 1
 </h3>
 <h2 class="estudio">
  Los holocaustos
 </h2>
 <span class="versiculo">
  <b>
   1
  </b>
 </span>
 <span class="texto">
  El Señor llamó a Moisés desde la tienda del encuentro, y le dijo lo siguiente:
 </span>
 <br/>
 <span class="versiculo">
  <b>
   2
  </b>
 </span>
 <span class="texto">
  «Habla con los israelitas y diles que cuando alguno me traiga ofrendas de animales, me las deberá traer de su ganado o de su rebaño.
 </span>
 <br/>
 <span class="versiculo">
  <b>
   3
  </b>
 </span>
 <span class="texto">
  »Si el animal que ofrece en holocausto es de su ganado, tendrá que ser un toro sin defecto. Para que le sea aceptado, deberá ofrecerlo en presencia del Señor a la entrada de la tienda del encuentro,
    """

main()

