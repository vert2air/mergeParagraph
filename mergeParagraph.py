
def flushBuf(buf, fw) :
    # buf にたまっている時だけ処理する。
    if len(buf) > 0 :
        print(buf.pop(0).rstrip(), file=fw, end='')
        for b in buf :
            print(' ', file=fw, end='')
            print(b.rstrip(), file=fw, end='')
        print('', file=fw)

def mergeParagraph(fr, fw, lineMaxLen) :
    buf = []
    for line in fr :
        if line.rstrip() == '' :
            # 空行だった。
            flushBuf(buf, fw)
            print('', file=fw)
            buf = []
        elif len(buf) == 0 :
            # buf が空なので、取り合えずbuffering
            buf.append(line)
        else :
            # bufの最後の行を見て、継続行かを判断する。
            ws = line.split()
            if (len(buf[-1]) + 1 + len(ws[0]) < lineMaxLen) :
                # 先頭の単語を前の行の後に付けても
                # 1行の最大文字数を超えないのなら
                # 意図的に改行していると判断し、
                # 今のbufまでの内容を吐き出す。この時改行もされる。
                flushBuf(buf, fw)
                buf = []
            buf.append(line)
    flushBuf(buf, fw)

from collections import defaultdict
def inferMaxLen(fr) :
    inferCnt = defaultdict(int)
    prevLen = 0
    for line in fr :
        line = line.rstrip()
        if line == '' : # 現在行が空行
            pass
        elif prevLen == 0 : # 前の行が空行
            pass
        else :
            fwLen = len(line.split()[0])
            for rLen in range(prevLen, prevLen + 1 + fwLen) :
                inferCnt[rLen] += 1
        prevLen = len(line)
    mostLen, mostCnt = -1, 0
    for iLen in sorted(inferCnt.keys()) :
        if inferCnt[iLen] >= mostCnt :
            mostLen, mostCnt = iLen, inferCnt[iLen]
        #print('{} => {}'.format(iLen, inferCnt[iLen]))
    return mostLen

fn = '20kLeaguesUnderTheSea_orig.txt'
fout = '20kLeaguesUnderTheSea_mP.txt'

with open(fn, 'r', encoding='utf8') as fr :
    lineMaxLen = inferMaxLen(fr)
    print('lineMaxLen = {}'.format(lineMaxLen))

with open(fn, 'r', encoding='utf8') as fr :
    with open(fout, 'w', encoding='utf8') as fw :
        mergeParagraph(fr, fw, lineMaxLen)

