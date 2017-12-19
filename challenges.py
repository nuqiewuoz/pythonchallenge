from urllib import parse, request
import pickle
import os
import zipfile
from PIL import Image
from PIL import ImageDraw
from PIL import ImageSequence
from PIL import ImageColor
import bz2
import gzip
import zlib
import xmlrpc
import re
from datetime import date
from http import cookiejar
import http.client
import codecs
import difflib
import base64
import wave
import pprint
import this
import numpy
import hashlib
import keyword
import csv
import itertools
from functools import reduce
from operator import mul
import math



def ch00():
    # 274877906944
    a = 2
    b = 38
    return a**b


def shift(ch, num=0, filter_char=False):
    """ a-z , A-Z
        shift "ch" to num character
    """
    a = ord('a')
    z = ord('z')
    A = ord('A')
    Z = ord('Z')
    asc = ord(ch)
    if a <= asc <= z:
        asc += num
        if asc < a:
            asc += 26
        if asc > z:
            asc -= 26
    elif A <= asc <= Z:
        asc += num
        if asc < A:
            asc += 26
        if asc > Z:
            asc -= 26
    else:
        if filter_char:
            if ch == ' ':
                return ch
            return ''
    return chr(asc)


def shiftstr(s, num):
    new_str = ""
    for ch in s:
        new_str += shift(ch, num)
    return new_str


def shift2(s):
    # map -> ocr
    from_str = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    to_str = "cdefghijklmnopqrstuvwxyzabCDEFGHIJKLMNOPQRSTUVWXYZAB"
    tran = str.maketrans(from_str, to_str)
    return s.translate(tran)


def ch01(num=2):
    raw_str = r"g fmnc wms bgblr rpylqjyrc gr zw fylb. rfyrq ufyr amknsrcpq ypc dmp. bmgle gr gl zw fylb gq glcddgagclr ylb rfyr'q ufw rfgq rcvr gq qm jmle. sqgle qrpgle.kyicrpylq() gq pcamkkclbcb. lmu ynnjw ml rfc spj."
    new_str = ""
    for ch in raw_str:
        new_str += shift(ch, num)
    return new_str


def ch02():
    # equality
    """
    read data from 'data2', filter words not in alphabet
    """
    new_str = ""
    with open('data2', 'r') as src:
        # for line in src.readlines():
        #     for ch in line:
        #         if ch.isalpha():
        #             new_str += ch
        new_str = ''.join(re.findall("[a-zA-Z]", src.read()))
    return new_str


def ch03():
    # linkedlist
    """
    read data from 'data3'
    """
    new_str = ""
    with open('data3', 'r') as src:
        # lines = src.readlines()
        # for aline in lines:
        #     line = aline.strip()
        #     for j in range(3, len(line)-3):
        #         ch = line[j]
        #         if ch.islower() and line[j - 3:j].isupper() and (j == 3 or line[j - 4].islower()) \
        #                 and line[j + 1:j + 4].isupper() and (j == len(line) - 4 or line[j + 4].islower()):
        #             new_str += ch
        text = src.read()
        new_str = ''.join(re.findall('[^A-Z][A-Z]{3}([a-z])[A-Z]{3}[^A-Z]', text))
    return new_str


def get_next_nothing(nid):
    url = parse.urlunparse(['http', 'www.pythonchallenge.com', '/pc/def/linkedlist.php', '', 'nothing={0}'.format(nid), ''])
    req = request.Request(url)
    newid = nid
    with request.urlopen(req) as response:
        bstr = response.read()
        newid = bstr.decode('ascii').split(' ')[-1]
    return newid


def get_page_bstr(page):
    url = r'http://www.pythonchallenge.com/pc/def/'+page
    req = request.Request(url)
    with request.urlopen(req) as response:
        result = response.read()
    return result


def get_return_page(page):
    un = "huge"
    pd = "file"
    result = get_page(r"return/"+page, un, pd, page)
    return result


def get_page(page, username, password, filename):
    url = r'http://www.pythonchallenge.com/pc/'+page
    password_mgr = request.HTTPPasswordMgrWithDefaultRealm()
    password_mgr.add_password(None, url, username, password)
    handler = request.HTTPBasicAuthHandler(password_mgr)
    opener = request.build_opener(handler)
    request.install_opener(opener)
    with request.urlopen(url) as response:
        result = response.read()
    with open(filename, 'wb') as f:
        f.write(result)
    return result


def open_page(page):
    url = r'http://www.pythonchallenge.com/pc/'+page
    req = request.Request(url)
    with request.urlopen(req) as response:
        result = response.read()
    return result


def ch04():
    nid = '12345'
    for i in range(500):
        print(nid)
        if nid.isdigit():
            nid = get_next_nothing(nid)
        else:
            if nid == 'going.':
                nid = get_next_nothing('8022')
            else:
                break
    return nid


def ch05():
    banner = get_page_bstr('banner.p')
    rows = pickle.loads(banner)
    with open('data5.txt', 'w') as file:
        lines = []
        for row in rows:
            line = ""
            for (ch, num) in row:
                line += ch * num
            line += os.linesep
            lines.append(line)
        file.writelines(lines)

    return "channel"


def ch06():
    # hockey: it's in the air. look at the letters.
    zf = get_page_bstr('channel.zip')
    with open('data6.zip', 'wb') as f:
        f.write(zf)

    z = zipfile.ZipFile('data6.zip')
    # from readme.txt start number is 90052
    nid = '90052'
    comments = b''
    while nid.isdigit():
        comments += z.getinfo(nid+'.txt').comment
        message = z.read(nid+'.txt').decode()
        nid = message.split(' ')[-1]
    print(comments.decode())
    return comments.decode()


def ch07():
    bimg = get_page_bstr('oxygen.png')
    with open('oxygen.png', 'wb') as f:
        f.write(bimg)
    img = Image.open('oxygen.png')
    w, h = img.size
    pwd = ''
    for i in range(w//7):
        r,g,b,a = img.getpixel((i*7, h/2))
        pwd += chr(r)
    print(pwd)
    pwd = ''
    for x in [105, 110, 116, 101, 103, 114, 105, 116, 121]:
        pwd += chr(x)
    return pwd


def ch08():
    """
    un: huge
    pd: file
    """
    username = bz2.decompress(b'BZh91AY&SYA\xaf\x82\r\x00\x00\x01\x01\x80\x02\xc0\x02\x00 \x00!\x9ah3M\x07<]\xc9\x14\xe1BA\x06\xbe\x084')
    password = bz2.decompress(b'BZh91AY&SY\x94$|\x0e\x00\x00\x00\x81\x00\x03$ \x00!\x9ah3M\x13<]\xc9\x14\xe1BBP\x91\xf08')
    return "un:"+username.decode()+"    pd:"+password.decode()


def ch09():
    get_return_page('good.jpg')
    first = [146,399,163,403,170,393,169,391,166,386,170,381,170,371,170,355,169,346,167,335,170,329,170,320,170,
             310,171,301,173,290,178,289,182,287,188,286,190,286,192,291,194,296,195,305,194,307,191,312,190,316,
             190,321,192,331,193,338,196,341,197,346,199,352,198,360,197,366,197,373,196,380,197,383,196,387,192,
             389,191,392,190,396,189,400,194,401,201,402,208,403,213,402,216,401,219,397,219,393,216,390,215,385,
             215,379,213,373,213,365,212,360,210,353,210,347,212,338,213,329,214,319,215,311,215,306,216,296,218,
             290,221,283,225,282,233,284,238,287,243,290,250,291,255,294,261,293,265,291,271,291,273,289,278,287,
             279,285,281,280,284,278,284,276,287,277,289,283,291,286,294,291,296,295,299,300,301,304,304,320,305,
             327,306,332,307,341,306,349,303,354,301,364,301,371,297,375,292,384,291,386,302,393,324,391,333,387,
             328,375,329,367,329,353,330,341,331,328,336,319,338,310,341,304,341,285,341,278,343,269,344,262,346,
             259,346,251,349,259,349,264,349,273,349,280,349,288,349,295,349,298,354,293,356,286,354,279,352,268,
             352,257,351,249,350,234,351,211,352,197,354,185,353,171,351,154,348,147,342,137,339,132,330,122,327,
             120,314,116,304,117,293,118,284,118,281,122,275,128,265,129,257,131,244,133,239,134,228,136,221,137,
             214,138,209,135,201,132,192,130,184,131,175,129,170,131,159,134,157,134,160,130,170,125,176,114,176,
             102,173,103,172,108,171,111,163,115,156,116,149,117,142,116,136,115,129,115,124,115,120,115,115,117,
             113,120,109,122,102,122,100,121,95,121,89,115,87,110,82,109,84,118,89,123,93,129,100,130,108,132,110,
             133,110,136,107,138,105,140,95,138,86,141,79,149,77,155,81,162,90,165,97,167,99,171,109,171,107,161,
             111,156,113,170,115,185,118,208,117,223,121,239,128,251,133,259,136,266,139,276,143,290,148,310,151,
             332,155,348,156,353,153,366,149,379,147,394,146,399]
    second = [156,141,165,135,169,131,176,130,187,134,191,140,191,146,186,150,179,155,175,157,168,157,163,157,159,
              157,158,164,159,175,159,181,157,191,154,197,153,205,153,210,152,212,147,215,146,218,143,220,132,220,
              125,217,119,209,116,196,115,185,114,172,114,167,112,161,109,165,107,170,99,171,97,167,89,164,81,162,
              77,155,81,148,87,140,96,138,105,141,110,136,111,126,113,129,118,117,128,114,137,115,146,114,155,115,
              158,121,157,128,156,134,157,136,156,136]
    img = Image.open('good.jpg')
    draw = ImageDraw.Draw(img)
    draw.line(list(zip(first[0::2],first[1::2])), "red")
    draw.line(list(zip(second[0::2],second[1::2])), "red")
    img.save('good1.jpg')
    return "bull"


def bull_array(s):
    news = ''
    current_ch = ''
    current_num = 0
    for ch in s:
        if current_ch == '':
            current_ch = ch
            current_num = 1
        else:
            if current_ch == ch:
                current_num += 1
            else:
                news += str(current_num)+current_ch
                current_ch = ch
                current_num = 1
    # print(news, current_ch)
    news += str(current_num)+current_ch
    return news


def ch10():
    """1, 11, 21, 1211, 111221,,,"""
    s = '1'
    for i in range(30):
        s = bull_array(s)
    return len(s)


def ch11():
    get_return_page('cave.jpg')
    newimg = Image.new('RGB', (320,480))
    img = Image.open('cave.jpg')
    w,h = img.size
    for i in range(w//2):
        for j in range(h):
            c = (0,0,0)
            if j % 2 == 0:
                c = img.getpixel((i*2,j))
            else:
                c = img.getpixel((i*2+1,j))
            newimg.putpixel((i,j), c)
    newimg.save('cave1.jpg')
    return "evil"


def ch12():
    get_return_page('evil2.gfx')
    with open('evil2.gfx', 'rb') as f:
        gfx = f.read()
        types = ['jpg', 'png', 'gif', 'png', 'jpg']
        for i in range(5):
            sf = open('evil2%d.%s' % (i, types[i]), 'wb')
            sf.write(gfx[i::5])
            sf.close()
    print(get_return_page('evil4.jpg'))
    return 'disproportional'


def ch13():
    phonebook = xmlrpc.client.ServerProxy('http://www.pythonchallenge.com/pc/phonebook.php')
    print(phonebook.system.listMethods())
    return phonebook.phone('Bert')


def ch14():
    get_return_page('wire.png')
    # shuffle bimg to 100*100
    img = Image.open('wire.png')
    answer = Image.new(img.mode, (100, 100), 0)
    # start = 0
    # for i in range(50):
    #     t= 100-i*2
    #     r = t-1
    #     b = t-1
    #     l = t-2
    #     for j in range(t):
    #         answer.putpixel((i,i+j), img.getpixel((start+j,0)))
    #     start += t
    #     for j in range(r):
    #         answer.putpixel((i+j+1,100-i-1), img.getpixel((start+j,0)))
    #     start += r
    #     for j in range(b):
    #         answer.putpixel((100-i-1,100-i-j-2), img.getpixel((start+j,0)))
    #     start += b
    #     for j in range(l):
    #         answer.putpixel((100-i-j-2,i), img.getpixel((start+j,0)))
    #     start += l
    dirs = [(1, 0), (0, 1), (-1, 0), (0, -1)]
    x, y, z = -1, 0, 0
    for i in range(200):
        d = dirs[i % 4]
        for j in range((200 - i) // 2):
            x += d[0]
            y += d[1]
            answer.putpixel((x, y), img.getpixel((z, 0)))
            z += 1
    answer.save('wire1.png')
    return "uzi"


def ch15():
    for i in range(100):
        if i % 2 == 1:
            year = 1006+i*10
            month = 1
            day = 26
            d = date(year,month,day)
            if d.isoweekday() == 1:
                print(d)
    return "mozart"


def ch16():
    get_return_page('mozart.gif')
    mark = 195
    offsets = []
    img = Image.open('mozart.gif')
    w,h = img.size
    for i in range(h):
        for j in range(w):
            if img.getpixel((j,i)) == mark:
                offsets.append((j,i))
                break
    new_img = Image.new(img.mode, img.size, 0)
    for i in range(h):
        for j in range(w):
            offset, y = offsets[i]
            new_img.putpixel((j,i), img.getpixel(((j+offset)%w, i)))
    new_img.putpalette(img.getpalette())
    new_img.save("mozart2.gif")
    return "romance"


def ch17():
    auth_handler = request.HTTPBasicAuthHandler()
    auth_handler.add_password('inflate', 'www.pythonchallenge.com', 'huge', 'file')
    jar = cookiejar.CookieJar()
    cookie_handler = request.HTTPCookieProcessor(jar)
    opener = request.build_opener(auth_handler, cookie_handler)
    opener.open('http://www.pythonchallenge.com/pc/def/linkedlist.php')
    hint = list(jar)[0].value
    print('hint:',hint)
    nid = '12345'
    cookies = ''
    while nid:
        url = 'http://www.pythonchallenge.com/pc/def/linkedlist.php?busynothing=%s' % nid
        r = opener.open(url)
        text = r.read().decode()
        s = re.search(r'and the next busynothing is ([0-9]+)', text)
        if len(list(jar)) > 0:
            cookies += list(jar)[0].value
        if not s:
            nid = None
            print('final:',text)
        else:
            nid = s.groups()[0]
    print(cookies)
    bm = request.unquote_to_bytes(cookies.replace('+', ' '))
    message = bz2.decompress(bm)
    print(message)
    phonebook = xmlrpc.client.ServerProxy('http://www.pythonchallenge.com/pc/phonebook.php')
    phonebook.phone('Leopold')
    list(jar)[0].value = 'the flowers are on their way'
    print(opener.open('http://www.pythonchallenge.com/pc/stuff/violin.php').read())
    return 'balloons'


def unhex(s):
    # return codecs.getdecoder('hex')(re.sub('[^0-9a-fA-F]', '', s))[0]
    return codecs.decode(re.sub('[^0-9a-fA-F]', '', s), 'hex')


def ch18():
    # goto brightness.html
    get_return_page('deltas.gz')
    gz = gzip.open('deltas.gz')
    lines = gz.readlines()
    lines1 = []
    lines2 = []
    for line in lines:
        twoline = line.split(b"   ")
        lines1.append((twoline[0]+b'\n').decode())
        lines2.append(twoline[1].decode())
    diffs = list(difflib.Differ().compare(lines1, lines2))
    pngs = [''.join(filter(lambda l: l[0] == d, diffs)) for d in " -+"]
    for i in range(len(pngs)):
        with open('deltas{0}.png'.format(i), 'wb') as f:
            f.write(unhex(pngs[i]))

    return '../hex/bin.html, butter, fly'


def ch19():
    bin = get_page('hex/bin.html', 'butter', 'fly', 'bin.html')
    # bin = open('bin.html','rb').read()
    b64 = re.search(b'base64\n\n(.*)\n\n', bin, re.DOTALL).groups(1)[0]
    with open('indian.wav', 'wb') as f:
        f.write(base64.decodestring(b64))

    iw = wave.open('indian.wav')
    iw2 = wave.open('indian2.wav','w')
    iw2.setnchannels(iw.getnchannels())
    iw2.setsampwidth(iw.getsampwidth())
    iw2.setframerate(iw.getframerate()//2)
    iw2.writeframes(iw.readframes(iw.getnframes())[::2])
    iw2.close()
    # then mail to leopold.moz@pythonchallenge.com with title "sorry"
    # get "md5: bbb8b499a0eef99b52c7f13f4e78c24b"
    # this is a hint for level 24...
    return "idiot"


def get_range(start, end, page='/pc/hex/unreal.jpg'):
    conn = http.client.HTTPConnection('www.pythonchallenge.com')
    headers = {'Authorization': 'Basic '+base64.b64encode(b'butter:fly').decode(),
               'Range': 'bytes={0}-{1}'.format(start, end)}
    conn.request('GET', page, '', headers)
    return conn.getresponse()


def next_range(start, starts, messages):
    r = get_range(start, 0)
    value = r.getheader('Content-Range')
    next_start = None
    if value:
        m = re.match(r'bytes ([0-9]+)-([0-9]+)/([0-9]+)',value)
        if m:
            next_start = int(m.group(2))+1
            starts.append(next_start)
            messages.append(r.read())
    return next_start


def ch20():
    # ('content-range', 'bytes 0-30202/2123456789'),
    starts = []
    messages = []
    start = 30203
    while start:
        start = next_range(start, starts, messages)
    print(starts)
    print(messages)
    hint = get_range(2123456789, 0).read()
    print(hint)
    print(get_range(2123456743, 0).read())
    bs = get_range(1152983631, 0).read()
    with open('idiot.zip', 'wb') as f:
        f.write(bs)
    print(hint[::-1])
    zf = zipfile.ZipFile('idiot.zip', 'r')
    zf.extractall('./idiot', pwd=b'redavni')
    with open('./idiot/readme.txt') as f:
        pprint.pprint(f.read())
    return ""


def iszlib(b):
    return b[:2] == b'x\x9c'


def isbz2(b):
    return b[:10] == b'BZh91AY&SY'


def ch21():
    # please
    f = open('./idiot/package.pack', 'rb')
    bstr = f.read()
    f.close()
    # zlib_list = []
    # bz2_list = []
    iscompressed = isbz2(bstr) or iszlib(bstr)
    bstr = zlib.decompress(bstr)
    logs = ""
    while iscompressed:
        if isbz2(bstr):
            # bz2_list.append(bstr)
            bstr = bz2.decompress(bstr)
            logs += 'b'
        elif iszlib(bstr):
            # zlib_list.append(bstr)
            bstr = zlib.decompress(bstr)
            logs += 'z'
        else:
            bstr = bstr[::-1]
            if isbz2(bstr):
                # bz2_list.append(bstr)
                bstr = bz2.decompress(bstr)
                logs += 'B'
            elif iszlib(bstr):
                # zlib_list.append(bstr)
                bstr = zlib.decompress(bstr)
                logs += 'Z'
            else:
                iscompressed = False
    print(bstr)
    pprint.pprint(logs.replace('z', ' ').split('Z'))
    return "copper"


def ch22():
    get_page('/hex/white.gif', 'butter', 'fly', 'white.gif')
    gif = Image.open('white.gif')
    frames = []
    positions = []
    for im in ImageSequence.Iterator(gif):
        # every image only have 1 none 0 point
        w1, h1, w2, h2 = im.getbbox()
        positions.append((w1-100, h1-100))
        frame = im.point(lambda i: i * 30)
        frames.append(frame)
    frames[0].save('white1.gif', save_all=True, append_images=frames[1:])
    gif.close()
    img = Image.new('RGB', (500,100), 0)
    draw = ImageDraw.Draw(img)
    startx, starty = (-50, 50)
    posx, posy = startx, starty
    for (x, y) in positions:
        if x == 0 and y == 0:
            startx += 100
            starty = 50
            posx, posy = startx, starty
        else:
            x1, y1 = posx + x, posy + y
            draw.line([(posx, posy), (x1, y1)], "red")
            posx, posy = x1, y1
    img.save('white1.png')
    return "bonus"


def ch23():
    #python zen
    print(shiftstr(this.s, 13))
    s = 'va gur snpr bs jung?'
    print(shiftstr(s, 13))
    return "ambiguity"


def iswhie(c):
    return c == ImageColor.getcolor('white', 'RGBA')


def ch24():
    m = load_maze()
    # resolve_maze(m, (0, 639), (640, 1))
    maze_file()
    return "lake"


def load_maze():
    get_page("/hex/maze.png", 'butter', 'fly', 'maze.png')
    img = Image.open('maze.png')
    w,h = img.size
    maze = []
    for i in range(h):
        line = []
        for j in range(w):
            if iswhie(img.getpixel((j,i))):
                line.append(1)
            else:
                line.append(0)
        maze.append(line)
    return maze


def draw_result(maze, path, name='maze2.png'):
    m = numpy.array(maze)
    l, r = m.shape
    img = Image.new('RGBA', m.shape, 0)
    # print(img.mode)
    # print(img.getcolors())
    for i in range(l):
        for j in range(r):
            c = ImageColor.getcolor('white', 'RGBA')
            if int(m[i,j]) == 1:
                c = ImageColor.getcolor('black', 'RGBA')
            img.putpixel((j,i), c)
    for p in path:
        img.putpixel((p[1], p[0]), ImageColor.getcolor('red', 'RGBA'))
    img.save(name)
    return ''


def resolve_maze(m, start, end):
    maze = numpy.array(m)
    dirs = [(-1, 0), (0, 1), (1, 0), (0, -1)]
    p = start
    if maze[end] == 1:
        return None
    path = [start]
    times = 0
    while p != end and len(path) > 0:
        if times % 1000 == 0:
            print(times)
        times += 1
        p = path[-1]
        find = False
        for d in dirs:
            np = (p[0]+d[0], p[1]+d[1])
            if np[0] >= maze.shape[0] or np[1] >= maze.shape[1] or np[0] < 0 or np[1] < 0:
                continue
            if np not in path and maze[np] == 0:
                path.append(np)
                p = np
                find = True
                break
        if not find:
            maze[p] = 1
            path.pop()
    with open('path.txt', 'w') as f:
        f.write(str(path))
    return path


def maze_file():
    with open('path.txt') as f:
        path = re.findall('([0-9]+), ([0-9]+)', f.read())

    img = Image.open('maze.png')
    reds = [img.getpixel((int(p[1]), int(p[0])))[0] for p in path[1::2]]
    bzip = bytes(reds)
    with open('maze.zip', 'wb') as f:
        f.write(bzip)
    if not os.path.isdir('maze'):
        os.mkdir('maze')
    z = zipfile.ZipFile('maze.zip')
    z.extractall('./maze')
    return bzip


def ch25():
    if not os.path.isdir('lake'):
        os.mkdir('lake')
    for i in range(1, 26):
        name = 'lake{0}.wav'.format(i)
        get_page('/hex/'+name, 'butter', 'fly', './lake/'+name)
        with wave.open('./lake/'+name) as wav:
            img = Image.frombytes('RGB', (60, 60), wav.readframes(wav.getnframes()))
            img.save('./lake/lake{0}.png'.format(i))

    jigsaw = Image.new('RGB', (300, 300), 0)
    for i in range(1,26):
        img = Image.open('./lake/lake{0}.png'.format(i))
        jigsaw.paste(img, (60*((i-1)%5), 60*((i-1)//5)))
        img.close()
    jigsaw.save('lakes.png')
    return 'decent'


def ch26():
    md5code = "bbb8b499a0eef99b52c7f13f4e78c24b"
    with open('./maze/mybroken.zip', 'rb') as f:
        broken = f.read()
        repair = broken
        for i in range(len(broken)):
            for ch in range(256):
                repair = broken[:i]+bytes([ch])+broken[i+1:]
                md5 = hashlib.md5()
                md5.update(repair)
                if md5.hexdigest() == md5code:
                    print('fix success:{0}, {1}'.format(i, bytes([ch])))
                    break
            else:
                continue
            break
        if repair != broken:
            with open('./maze/repair.zip', 'wb') as nf:
                nf.write(repair)
            z = zipfile.ZipFile('./maze/repair.zip')
            print(z.filelist)
            z.extractall()
    return "speedboat"


def ch27():
    get_page('/hex/zigzag.gif', 'butter', 'fly', 'zigzag.gif')
    img = Image.open('zigzag.gif')
    palette = img.palette.getdata()[1][::3]
    imgbytes = img.tobytes()
    trans = bytes.maketrans(bytes(range(256)), palette)
    imgtrans = imgbytes.translate(trans)
    #hint
    im = Image.new('1', img.size, 0)
    im.putdata([p[0] == p[1] for p in zip(imgbytes[1:], imgtrans[:-1])])
    im.save('zigclue.png')

    deltas = filter(lambda p: p[0] != p[1], zip(imgbytes[1:], imgtrans))
    bzbytes = bytes([p[0] for p in deltas])
    bwords = bz2.decompress(bzbytes)
    wordset = set(bwords.decode().split(' '))
    for word in wordset:
        if word != r'../ring/bell.html' and not keyword.iskeyword(word): #and word not in dir('__builtin__')
            print(word)
    return "repeat, switch"


def ch28():
    get_page('/ring/bell.png', 'repeat', 'switch', 'bell.png')
    img = Image.open('bell.png')
    rs, gs, bs = img.split()
    w, h = img.size
    deltas = []
    for i in range(w//2):
        for j in range(h):
            g1 = gs.getpixel((i*2, j))
            g2 = gs.getpixel((i*2+1, j))
            deltas.append(abs(g1-g2))
    message = bytes(filter(lambda d: d % 42 != 0, deltas))
    print(message)
    return "guido"


def ch29():
    bs = get_page('/ring/guido.html', 'repeat', 'switch', 'guido.html')
    end = b'</html>\n'
    endpos = bs.rindex(end)+len(end)
    lines = bs[endpos:].split(b'\n')
    counts = []
    for l in lines:
        counts.append(len(l))
    message = bz2.decompress(bytes(counts))
    print(message)
    return "yankeedoodle"


def ch30():
    b = get_page('/ring/yankeedoodle.csv', 'repeat', 'switch', 'yankeedoodle.csv')
    nb = b.replace(b',\n', b'\n')
    with open('yankeedoodle.csv', 'wb') as f:
        f.write(nb)
    numbers = []
    with open('yankeedoodle.csv') as f:
        reader = csv.reader(f, quoting=csv.QUOTE_NONNUMERIC)
        for line in reader:
            numbers.extend(line)
    length = len(numbers)
    factors = simple_prime_factor(length)
    h, w = factors[0], factors[1]
    img = Image.new('L', (w, h), 0)
    for i in range(length):
        img.putpixel((i//h, i%h), int(numbers[i]*256))
    img.save('yankee.png')
    message = []
    for i in range(length//3):
        n = "{:.5f}".format(numbers[3*i])[5]+"{:.5f}".format(numbers[3*i+1])[5]+"{:.5f}".format(numbers[3*i+2])[6]
        message.append(int(n))
    print(bytes(message)[:200])
    return "grandpa"


def simple_prime_factor(n):
    factors = []
    while n > 2:
        for i in range(2, n//2):
            if n % i == 0:
                factors.append(i)
                n = n // i
                break
        else:
            # its a prime
            factors.append(n)
            break
    return factors


def ch31():
    # kohsamui, thailand
    get_page('/rock/mandelbrot.gif', 'kohsamui', 'thailand', 'mandelbrot.gif')
    draw_mandelbrot_fractal()
    img = Image.open('mandelbrot.gif')
    img2 = Image.open('mandelbrot2.gif')
    data1 = list(img.getdata())
    data2 = list(img2.getdata())
    deltas = [a-b for a, b in zip(data1, data2) if a != b]
    p = simple_prime_factor(len(deltas))

    img3 = Image.new('1', (p[0], p[1]), 0)
    img3.putdata([i > 0 for i in deltas])
    img3.save('mandelbrot3.gif')
    return 'arecibo'


def draw_mandelbrot_fractal(left=0.34, top=0.57, width=0.036, height=0.027, iters=128, outfile='mandelbrot2.gif'):
    img = Image.open('mandelbrot.gif')
    im = Image.new(img.mode, img.size, 0)
    im.putpalette(img.getpalette())

    w, h = img.size

    for i in range(w):
        for j in range(h):
            x = left + width * i / w
            y = top + height * j / h
            m = mandelbrot(complex(x,y), iters)
            im.putpixel((i, h-j-1), m)
    im.save(outfile)
    return outfile


def mandelbrot(c, iter):
    z = complex(0)
    for i in range(iter):
        z = z * z + c
        if abs(z) > 2:
            return i
    return 127


def ch32():
    get_page('/rock/warmup.txt', 'kohsamui', 'thailand', 'warmup.txt')
    get_page('/rock/up.txt', 'kohsamui', 'thailand', 'up.txt')
    r, c, rows, columns = load_etch('up.txt')
    rowsets_list = [one_etch_set(row, c) for row in rows]
    ll1 = [len(s) for s in rowsets_list]
    print(ll1, sum(ll1), reduce(mul, ll1))
    columnsets_list = [one_etch_set(column, r) for column in columns]
    ll2 = [len(s) for s in columnsets_list]
    print(ll2, sum(ll2), reduce(mul, ll2))
    eas, rl, cl = eas_mathod(r, c, rowsets_list, columnsets_list)
    pprint.pprint(eas)
    # pprint.pprint(simple_eas_method(r,c,rowsets_list, columnsets_list))
    # “free” as in “free speech,” not as in “free beer”
    return "python, beer"


def eas_mathod(row_num, col_num, possible_row_list, possible_col_list, eas=[]):
    result = ['.'*col_num for i in range(row_num)]
    if len(eas) > 0:
        result = eas.copy()
    row_list = possible_row_list.copy()
    col_list = possible_col_list.copy()
    for n in itertools.count(1):
        update_row = 0
        # update rows
        for i in range(row_num):
            rowset = row_list[i]
            num = len(rowset)
            for j in range(col_num):
                count = 0
                for row in rowset:
                    if row[j] == '1':
                        count += 1
                if count == num and result[i][j] != '1':
                    # the r[i][j] should be 1
                    update_row += 1
                    result[i] = result[i][:j]+'1'+result[i][j+1:]
                elif count == 0 and result[i][j] != '0':
                    update_row += 1
                    result[i] = result[i][:j]+'0'+result[i][j+1:]
        print('update rows:', update_row)
        update_col = 0
        #update columns
        for j in range(col_num):
            colset = col_list[j]
            num = len(colset)
            for i in range(row_num):
                count = 0
                for col in colset:
                    if col[i] == '1':
                        count += 1
                if count == num and result[i][j] != '1':
                    update_col += 1
                    result[i] = result[i][:j]+'1'+result[i][j+1:]
                elif count == 0 and result[i][j] != '0':
                    update_col += 1
                    result[i] = result[i][:j]+'0'+result[i][j+1:]
        print('update cols:', update_col)
        if update_row != 0 or update_col != 0:
            # filter the possible list with updated result
            new_row_list = row_list.copy()
            for i in range(row_num):
                rowset = row_list[i]
                pat= result[i]
                remove_row = set()
                for row in rowset:
                    if not re.match(pat, row):
                        remove_row.add(row)
                new_row_list[i] = rowset.difference(remove_row)
            new_col_list = col_list.copy()
            for j in range(col_num):
                colset = col_list[j]
                pat = ''.join(row[j] for row in result)
                remove_col = set()
                for col in colset:
                    if not re.match(pat, col):
                        remove_col.add(col)
                new_col_list[j] = colset.difference(remove_col)
            row_list = new_row_list
            col_list = new_col_list
        else:
            break
    ll1 = [len(s) for s in row_list]
    print(ll1, sum(ll1), math.log10(reduce(mul, ll1)))
    ll2 = [len(s) for s in col_list]
    print(ll2, sum(ll2), math.log10(reduce(mul, ll2)))
    return result, row_list, col_list


def simple_eas_method(r, c, rowsets_list, columnsets_list):
    counts = [list(range(len(s))) for s in rowsets_list]
    it = itertools.product(*counts)
    result = []
    for l in it:
        rowlist = [list(rowsets_list[i])[l[i]] for i in range(r)]
        for i in range(c):
            col = ''.join([row[i] for row in rowlist])
            if col not in columnsets_list[i]:
                # if one column is not correct break
                break
        else:
            # match all columns
            result = rowlist
            break
    return result

def load_etch(filename):
    with open(filename) as f:
        lines = f.readlines()
        cleanlines = [line.replace('\n', '') for line in filter(lambda l:l != '\n', lines)]
        d = '# Dimensions'
        dline = cleanlines.index(d)+1
        row, column = [int(s) for s in cleanlines[dline].split(' ')]
        # h = '# Horizontal'
        hstart = dline+2 #cleanlines.index(h)+1
        rows = []
        for i in range(row):
            r = [int(s) for s in cleanlines[hstart+i].split(' ')]
            rows.append(r)
        # v = '# Vertical'
        vstart = hstart+row+1 #cleanlines.index(v)+1
        columns = []
        for i in range(column):
            c = [int(s) for s in cleanlines[vstart+i].split(' ')]
            columns.append(c)
    return row, column, rows, columns


def one_etch_set(row, bits=9):
    v = bits - sum(row) - len(row) + 1
    s1 = '0'*v
    # replace "111" to a unique char
    unique_row = list(map(lambda x: chr(ord('A')+x), range(len(row))))
    s2 = ''.join([c+'0' for c in unique_row])[:-1]
    sets = combine_two_strings(s1, s2)
    result = set()
    # replace the unique char to original '1' sequence
    for s in sets:
        ns = s
        for i in range(len(row)):
            ns = ns.replace(unique_row[i], '1'*row[i])
        result.add(ns)

    return result


def combine_two_strings(s1, s2):
    # combine two strings in sequence
    # return all possible result
    # eg: combine 'ab' and 'cd'
    #     return {'abcd', 'acbd', 'acdb', 'cabd', 'cadb', 'cdab'}
    if s1 == '':
        return set([s2])
    if s2 == '':
        return set([s1])
    c1 = s1[0]
    c2 = s2[0]
    sets = set()
    set1 = combine_two_strings(s1[1:], s2)
    for s in set1:
        sets.add(c1+s)
    set2 = combine_two_strings(s1, s2[1:])
    for s in set2:
        sets.add(c2+s)
    return sets


def ch33():
    get_page('/rock/beer2.png', 'kohsamui', 'thailand', 'beer2.png')
    img = Image.open('beer2.png')
    data = list(img.getdata())
    m = max(data)
    valids = []
    for i in range(m, 0, -1):
        ash_data = list(filter(lambda x:x<i, data))
        num = len(ash_data)
        if math.sqrt(num).is_integer():
            sqrt_root = int(math.sqrt(num))
            print(sqrt_root)
            if sqrt_root not in valids and sqrt_root > 0:
                valids.append(sqrt_root)
                new_img = Image.new(img.mode, (sqrt_root, sqrt_root))
                new_img.putdata(ash_data)
                new_img.save('beer2_{}.png'.format(sqrt_root))

    return "gremlins"


def answers():
    print("0: {0}".format(ch00()))
    print("1:", shift2("map"))
    print("2:", ch02())
    print("3:", ch03())
    print("4:", "peak.html")
    print("5:", ch05())
    print("6:", "oxygen")
    print("7:", "integrity")
    print("8:", ch08())
    print("9:", "bull")
    print("10:", ch10())
    print("11:", ch11())
    print("12:", "disproportional")
    print("13:", "italy")
    print("14:", "uzi")
    print("15:", "mozart")
    print("16:", "romance")
    print("17:", "balloons")
    print("18:", '../hex/bin.html, butter, fly')
    print("19:", "idiot2")
    print("20:")
    print("21:", "copper")
    print("22:", "bonus")
    print("23:", "ambiguity")
    print("24:", "lake")
    print("25:", "decent")
    print("26:", "speedboat")
    print("27:", "un:repeat, pd:switch")
    print("28:", "guido")
    print("29:", "yankeedoodle")
    print("30:", "grandpa")
    print("31:", "arecibo")
    print("32:", "python, beer")
