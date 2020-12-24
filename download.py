import re

import shutil
import urllib.request as request
from contextlib import closing
from zipfile import ZipFile

import os
from bs4 import BeautifulSoup, NavigableString
from string import ascii_uppercase
import codecs
import pickle

# with closing(request.urlopen('ftp://ftp.gnu.org/gnu/gcide/gcide-latest.zip')) as r:
#     with open('gcide.zip', 'wb') as f:
#         shutil.copyfileobj(r,f)

# with ZipFile('gcide.zip','r') as f:
#     f.extractall('gcide')

directory = os.listdir("gcide")[0]

dictionary = {}
# for letter in ascii_uppercase:
#     with codecs.open('gcide/' + directory + '/CIDE.' + letter, 'r', encoding='utf-8', errors='ignore') as f:
#         text = f.read()
#         soup = BeautifulSoup(text, features = "html.parser")
#         with open(letter + ".p", "wb") as f:
#             pickle.dump(soup,f)

for letter in ascii_uppercase[:1]:
    with codecs.open('gcide/' + directory + '/CIDE.' + letter, 'r', encoding='utf-8', errors='ignore') as f:
        text = f.read()
        text = re.sub(r'<br/','',text)
        text = re.sub(r'<rj>(.*?)</rj>','\1',text)
        soup = BeautifulSoup(text, features = "html.parser")
    # with open(letter + ".p", "rb") as f:
    #     soup = pickle.load(f)
        entry_name = None
        entry = {}
        quotation = {}
        for p in soup.find_all('p')[0:100]:
            print(p.ent)
            print(p.text)
            for c in p.children:
                if type(c) == NavigableString:
                    continue
                if c.name == 'ent':
                    if entry_name != None:
                        if(entry_name in dictionary.keys() and
                            dictionary[entry_name] is not None):
                            dictionary[entry_name].append(entry)
                        else:
                            dictionary[entry_name] = [entry]
                    entry = {}
                    entry_name = c.text
                elif c.name == 'hw':
                    if c.text != entry_name:
                        raise Exception
                elif c.name == 'pos':
                    entry.setdefault
                    entry['pos'] = c.text
                elif c.name == 'sn':
                    entry['number'] = c.text
                elif c.name == 'def':
                    entry['def'] = c.text
                elif c.name == 'q':
                    quotation = {}
                    quotation['text'] = c.text
                elif c.name == 'qau':
                    quotation['author'] = c.text
                    if('quotes' in entry.keys() and 
                        entry['quotes'] is not None):
                        entry['quotes'].append(quotation)
                    else:
                        entry['quotes'] = [quotation]
                    entry['quotes']
                elif c.name == 'syn':
                    text = c.b.next_sibling.strip()
                    entry['syn'] = [t.strip() for t in text.split(",")]
                elif c.name == 'source':
                    if('sources' in entry.keys() and
                        entry['sources'] is not None):
                        entry['sources'].append(c.text)
                    else:
                        entry['sources'] = [c.text]
                elif c.name == 'pr':
                    entry['pronunciation'] = c.text
                elif c.name == 'mark':
                    entry['mark'] = c.text
                elif c.name == 'centered':
                    continue
                else:
                    print(c.name)
                    raise Exception

# with open('temp.xml','r') as f:
#     text = f.read()
#     soup = BeautifulSoup(text, features = "lxml")
#     for p in soup.find_all('p'):
#         print(p.children[0].name)