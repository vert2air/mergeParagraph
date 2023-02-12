
lineMaxLen = 71

def flushBuf(buf, fw) :
    # buf にたまっている時だけ処理する。
    if len(buf) > 0 :
        print(buf.pop(0).rstrip(), file=fw, end='')
        for b in buf :
            print(' ', file=fw, end='')
            print(b.rstrip(), file=fw, end='')
        print('', file=fw)

def mergeParagraph(fr, fw) :
    buf = []
    for line in fr :
        if line.rstrip() == '' :
            # 空行だった。
            flushBuf(buf, fw)
            print('', file=fw)
            buf = []
        else :
            if len(buf) == 0 :
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

fn = '20kLeaguesUnderTheSea_orig.txt'
fout = '20kLeaguesUnderTheSea_mP.txt'
with open(fn, 'r', encoding='utf8') as fr :
    with open(fout, 'w', encoding='utf8') as fw :
        mergeParagraph(fr, fw)

