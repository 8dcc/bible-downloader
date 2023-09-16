#!/usr/bin/python3

try:
    import sys, math, requests, bs4
except Exception:
    print("Please install the dependencies with:")
    print("  python3 -m pip install -r requirements.txt")
    exit(1)

##########################
RECURSE      = True       # Will go to the next chapter until finished
UPPER_TITLES = False      # Chapter titles in uppercase
VERSION      = "dhh"      # Bible version.
FIRST_BOOK   = "genesis"  # Only used for replacing START_URL
FIRST_CHAP   = "1"        #
##########################

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36"
BASE_URL   = "https://www.biblia.es/"
START_URL  = BASE_URL + f"biblia-buscar-libros-1.php?libro={FIRST_BOOK}&capitulo={FIRST_CHAP}&version={VERSION}"

def main():
    # Org header
    print("#+title: Bible")
    print("#+startup: overview")
    print("#+options: toc:2")
    print("#+author: 8dcc")

    # Add the following line if you want subscripts. Replace cursives with:
    # "^{" and "}"
    #print("#+options: ^:{}")

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

        # Used to check indentation for multi-line list items
        vers_num = 0

        for item in contents[1].find_all(["h3", "h2", "span"]):
            if (item.get("class") == None):
                continue

            if (item.get("class")[0] == "capitulo"):
                sys.stdout.write("\n** ")
                
                if (UPPER_TITLES):
                    print(item.string.upper())
                else:
                    print(item.string)

                sys.stdout.write('\n')
            elif (item.get("class")[0] == "estudio"):
                if (last_printed != "capitulo"):
                    sys.stdout.write('\n')

                print("*" + item.string + "*")
                sys.stdout.write('\n')
            elif (item.get("class")[0] == "versiculo"):
                # Split to convert "14-15" -> "14"
                final_vers = item.string.split("-")[0]

                # Add leading zero to <10
                if (int(final_vers) < 10):
                    final_vers = "0" + final_vers

                sys.stdout.write(final_vers)
                sys.stdout.write(". ")

                # Store current number for indentation
                vers_num = int(final_vers)
            elif (item.get("class")[0] == "texto"):
                # In theory we just printed the number
                for s in item.strings:
                    final_str = str(s).replace(chr(0x2014), "- ").replace("\r\n", "")

                    # No line limit since we can "SPC t w"

                    # Add space if more than one line in the same list item
                    if (last_printed == "texto"):
                        # Indentation for multi-line list items
                        digits_vers = int(math.log10(vers_num)) + 1

                        # Add leading zero to <10
                        if (digits_vers < 2):
                            digits_vers = 2

                        for i in range(digits_vers + 2):   # + space and dot
                            sys.stdout.write(' ')

                        print(final_str)
                    else:
                        print(final_str)

                    last_printed = "texto"

            last_printed = item.get("class")[0]

main()

