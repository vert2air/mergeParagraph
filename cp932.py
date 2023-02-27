import re
from collections import defaultdict

cp932_stat = defaultdict(int)

cp932_chars = {
    # short desc           REGEX     cp932
    'c Cedille'        : [ r'\xe7',   "c" ],
    'e accent grave'   : [ r'\xe8',   "e" ],  # 抑音符付き
    'e accent aigu'    : [ r'\xe9',   "e" ],  # アクセント記号付き
    'EM dash'          : [ r'\u2014', '-' ],
    'single backquote' : [ r'\u2018', "`" ],
    'single quote'     : [ r'\u2019', "'" ],  # <81>f  <81><66>
    #'double backquote' : [ r'\u201c', "``" ], # <81>g  <81><67>
    #'double quote'     : [ r'\u201d', "''" ], # <81>h  <81><68>
    'Bullet'           : [ r'\u2022', "・" ],
    'Trade Mark'       : [ r'\u2122', 'TM' ],

    'degree'           : [ r'\xb0', '°' ],    # 度 <81><88>

    #'ring above1'      : [ r'\u00BA', '度' ],
    #'ring above'       : [ r'\u02da', '度' ],

    'ampersand'       : [ r'&amp;',   '&' ],
}

def useCp932(line) :
    global cp932_stat, cp932_chars

    for desc, reg_cp in cp932_chars.items() :
        (line, n) = re.subn(reg_cp[0], reg_cp[1], line)
        cp932_stat[desc] += n
    return line

def getPtag(fr) :
    cnt = 0
    resP = []
    notP = []
    for line in fr :

        line = useRegChar(line)

        if re.search(r'<p>.*<p>', line) :
            # 一行に<p>が2個以上あったら、サポート外。
            raise ValueError('Double p tag')
        if re.search(r'<p>', line) :
            cnt += 1

        m = re.search(r'(<p>(.*)</p>)', line)
        if m is not None :
            # 一行の中で、<p>～</p> が収まるパターンが多数あったので、その処理
            resP.append(m.group(2))
            line = re.sub(r'(<p>(.*)</p>)', '', line)
            notP.append(line)

        elif re.search(r'^<p>$', line) :
            # ある行が <p> だけで、次の行が 本文+</p> というパターンに
            # Chapter開始直後がなっていたので、その処理
            nline = next(fr)
            nline = useRegChar(nline)
            m = re.search(r'^((.*)</p>)', nline)
            if m is not None :
                resP.append(m.group(2))
                nline = re.sub(r'((.*)</p>)', '', nline)
            notP.append('')    # lineに対応だが、<p>だけなので、空行出力
            notP.append(nline)

        else :
            # それ以外は、取り合えず何もしない。
            notP.append(line)

    '''
    print('& =>{}'.format(rep_amp))
    print('"-" =>{}'.format(rep_hy))
    print("c with , =>{}".format(rep_c_))
    print("e with ` =>{}".format(rep_e3))
    print("e with ' =>{}".format(rep_e2))
    print("・ =>{}".format(rep_blt))
    print("TM =>{}".format(rep_tm))
    print("` =>{}".format(rep_bq))
    print("' =>{}".format(rep_sq))
    print("`` =>{}".format(rep_lq))
    print("'' =>{}".format(rep_rq))
    '''

    return cnt, resP, notP

if __name__ == '__main__' :
    import sys

    fn = '2016830146115086814_2488-h-0.htm.xhtml'
    fn = sys.argv[1]

    with open(fn, 'r', encoding='utf8') as fr :
        success, resP, notP = getPtag(fr)
        for p in resP : print(p)
        #for p in notP : print(p, end='')
        print('result = {}'.format(success))
        for desc, stat in cp932_stat.items() :
            print('{} => {}'.format(desc, stat))

