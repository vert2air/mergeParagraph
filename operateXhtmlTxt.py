
import sys
from bs4 import BeautifulSoup, NavigableString, Tag
from cp932 import useCp932

def extract(soup, repl=[]) :
    ans = []
    ps = soup.select('p')
    for i, p in enumerate(ps) :
        #print('-------------- {} --------------'.format(i))
        for j, ct in enumerate(p.contents) :
            #print(type(ct))
            if type(ct) is NavigableString :
                # <p>タグの内容として、直接文字列が書かれていた。
                if len(repl) > 0 :
                    lcnt = ct.count('\n') + 1
                    #print('insert {} lines'.format(lcnt))
                    #for i in range(lcnt) :
                        #print(repl[i])
                        #print('\n'.join( repl[ : lcnt] ))
                    # ↓ここ、実際には、insertされない。
                    p.insert(j, '\n'.join( repl[ : lcnt] ))
                    #p.contents[j].replace_with(
                    #ct.string = '\n'.join( repl[ : ct.count('\n') + 1] )
                    del repl[ : lcnt]
                else :
                    ans.extend( useCp932(str(ct)).split('\n') )

            elif type(ct) is Tag and ct.name == 'a' :
                # <p>タグの内容として、<a>タグが含まれていた。
                for k, c_in_a in enumerate(ct.contents) :
                    # <p>タグ内の<a>タグの内容check
                    if type(c_in_a) is NavigableString :
                        if len(repl) > 0 :
                            #c_in_a.string = '\n'.join(
                            ct.contents[k] = '\n'.join(
                                    repl[ : c_in_a.count('\n') + 1] )
                            del repl[ : c_in_a.count('\n') + 1]
                        else :
                            ans.extend( useCp932(str(c_in_a)).split('\n') )
                    #else :
                        #print('  in<A>in<p> extraTAG : {}'.format(ct))
            #else :
                # <p>タグの内容として、文字列でも<a>でもないタグが含まれていた
                #print('in<p> extraTAG : {}'.format(ct))
    return ans, soup

fnSource = sys.argv[1]
fnXlated = sys.argv[2] if len(sys.argv) > 2 else ''

with open(fnSource, 'r', encoding='utf8') as fs :
    xhtml = fs.read()
soup = BeautifulSoup(xhtml, "html.parser")
if fnXlated == '' :
    ans, _ = extract(soup)
    for a in ans :
        print(a)
else :
    with open(fnXlated, 'r', encoding='utf8') as fx :
        xlated = fx.read().split('\n')
    #for i, l in enumerate(xlated) :
        #print('{} {}'.format(i, l))
    #print('------------------------------------------------------')
    _, soup = extract(soup, repl=xlated)
    with open('out.xhtml', 'w', encoding='utf8') as fw :
        fw.write(soup.prettify())
    #print(soup.prettify())


