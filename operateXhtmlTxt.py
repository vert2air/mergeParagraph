
import sys
from bs4 import BeautifulSoup, NavigableString, Tag
from bs4.formatter import HTMLFormatter
from cp932 import useCp932

def extract(soup, tag_name, repl=[]) :
    '''
    tag_name : name of tag to extract or replace strings in it. ex) 'p'
    '''
    tidx = -1 if repl == [] else 0
    ans = []
    while True :
        replaced = False
        tags = soup.select(tag_name)
        cidx = 0
        for i, tg in enumerate(tags) :
            for j, ct in enumerate(tg.contents) :
                if type(ct) is NavigableString :
                    # <tag_name>タグの内容として、直接文字列が書かれていた。
                    xs = useCp932(str(ct)).split('\n')
                    if len(repl) > 0 :
                        if cidx == tidx :
                            lcnt = len(xs)
                            tg.contents[j].replace_with('\n'.join(repl[ :lcnt]))
                            del repl[ : lcnt]
                            replaced = True
                            cidx += 1
                            break
                    else :
                        ans.extend( xs )
                    cidx += 1
                if tidx >= 0 and cidx > tidx :
                    break
            if tidx >= 0 and cidx > tidx :
                break
        if repl == [] or not replaced :
            break
        tidx += 1
    return ans, soup

fnSource = sys.argv[1]
fnXlated = sys.argv[2] if len(sys.argv) > 2 else ''

tags = [ 'p', 'a', 'h3' ]
with open(fnSource, 'r', encoding='utf8') as fs :
    xhtml = fs.read()
soup = BeautifulSoup(xhtml, "html.parser")
if fnXlated == '' :
    for tag in tags :
        ans, _ = extract(soup, tag)
        for a in ans :
            print(a)
else :
    with open(fnXlated, 'r', encoding='utf8') as fx :
        xlated = fx.readlines()
    for tag in tags :
        _, soup = extract(soup, tag, repl=xlated)
    with open('out.xhtml', 'w', encoding='utf8') as fw :
        #fw.write(soup.prettify(formatter='minimal'))
        fw.write(soup.prettify(formatter='html'))
        #formatter = HTMLFormatter(indent=2)
        #fw.write(soup.prettify(formatter=formatter))

