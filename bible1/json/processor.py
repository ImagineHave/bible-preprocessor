import json
import io
from pprint import pprint
import requests

with open('key_english.json') as bookkey:
    bkData  = json.load(bookkey)
 
with open('key_genre_english.json') as genreKey:
    gkData  = json.load(genreKey)
    
with open('testbible2.json') as bible:
    bData  = json.load(bible)
    

#pprint(bkData)
#pprint(gkData)
#pprint(bData)

def getGenre(genreNumber):
    for genre in gkData:
        if genre['g'] == genreNumber:
            return genre['n']

def getBookData(booknumber):
    for book in bkData:
        if book['b'] == booknumber:
            return (getGenre(book['g']),book['n'])

def processFields():
    l = []
    for f in bData['resultset']['row']:
        field = f['field']
        bookNumber = field[1]
        genre, book = getBookData(bookNumber)
        d = {'genre':genre, 'book':book, 'chapter':field[2], 'verse':field[3], 'passage':field[4]}
        l.append(d)
    return l
        
data = {}
data['bible'] = processFields()

try:
    to_unicode = unicode
except NameError:
    to_unicode = str

with io.open('result.json', 'w', encoding='utf8') as outfile:
    str_ = json.dumps(data,
                      indent=4, sort_keys=True,
                      separators=(',', ': '), ensure_ascii=False)
    outfile.write(to_unicode(str_))
    
r = requests.post('https://flask4j-cwih.c9users.io/feeder/upload', data=data)
print(r)
r = requests.get('https://flask4j-cwih.c9users.io/feeder/load')
print(r)


