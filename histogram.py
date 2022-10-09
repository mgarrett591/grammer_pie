# To use this file, you will need a sqlite database file with a histogram table compatible with mine.
# you can use my db init script
# I recommend using installing sqlitebrowser and zimdump
# You can get a zim file from https://library.kiwix.org or https://dumps.wikimedia.org/other/kiwix/zim/wikipedia
# zim files released from these locations are generally licensed under Attribution-ShareAlike 4.0 International (https://creativecommons.org/licenses/by-sa/4.0/legalcode)
# Please read the license, and make sure to include all necessary attributions when distributing the resulting sqlite database file

"""
--db init code
CREATE TABLE "histogram" (
	"spelling"	TEXT NOT NULL UNIQUE,
	"occurrences"	INTEGER DEFAULT 0,
	PRIMARY KEY("spelling")
)
"""

import os
import sqlite3

histo = {}
histo_list = []

Hangul_Jamo = range(0x1100,0x11ff + 1)
Hangul_Syllables = range(0xac00,0xd7a3 + 1)
Hangul_Jamo_Extended_A = range(0xa960,0xa97c + 1)
Hangul_Jamo_Extended_B = range(0xd7b0, 0xd7fb + 1)
Hangul_Compatibility_Jamo = range(0x3131, 0x318e + 1)

def inCharacterSet(letter):
    codepoint = ord(letter)
    return codepoint in Hangul_Jamo or codepoint in Hangul_Syllables or codepoint in Hangul_Jamo_Extended_A or codepoint in Hangul_Jamo_Extended_B or codepoint in Hangul_Compatibility_Jamo
    
def count(word):
    if(word == ''):
        pass
    elif word in histo.keys():
        histo[word] +=1
    else:
        histo[word] = 1

def scan_text(text):
    token = ""
    for letter in text:
        if(inCharacterSet(letter)):
            token += letter
        else:
            count(token)
            token = ""
    
def process_file(path):
    raw_html = ""
    try:
        with open(path) as f:
            raw_html = f.read()
    except UnicodeDecodeError:
        print("Skiping:",path)
    scan_text(raw_html)
    

def outer_loop(dump_path):
    for root, dir, files in os.walk(dump_path):
        for file in files:
            if (os.path.splitext(file)[1] not in {'pdf','exe','svg'}):
                process_file(os.path.join(root,file))

def sort_key(tup):
    return tup[1]

def commit_to_db(histo_list,DBPath):
    con = sqlite3.connect(DBPath)
    cur = con.cursor()
    cur.executemany("INSERT into histogram (spelling, occurrences) VALUES (?,?)",histo_list)
    con.commit()
    con.close()
            
sqliteDB = input('Path to sqlite file?')
dump_dir = input('Path to Wikipidia dump?')

outer_loop(sqliteDB)
histo_list = list(histo.items())
histo_list.sort(key=sort_key,reverse=True)

commit_to_db(histo_list, dump_dir)

#for item in histo_list:
#    print(item[0],item[1],sep=': ')