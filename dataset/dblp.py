from lxml import etree
import re

items = []
regex = r'^conf/.+/\d+$'
proceedings_list = []

def fast_iter(context, func):
    for event, elem in context:
        func(elem)
        elem.clear()
        while elem.getprevious() is not None:
            del elem.getparent()[0]
    del context

def parse_elem(elem):
    inproceedings = {'authors':[], 'title':'', 'proceedings':''}
    for child in elem.iterchildren():
        if child.tag == 'author':
            inproceedings['authors'].append(child.text)
        if child.tag == 'title':
            inproceedings['title'] = child.text
        if child.tag == 'crossref' and re.match(regx, child.text):
            tmp = child.text.split('/')
            inproceedings['proceedings'] = tmp[1]
            inproceedings['year'] = int(tmp[2])
    if 2010 >= inproceedings['year'] >= 2000 and inproceedings['proceedings'] in proceedings_list:
        items.append(inproceedings)
            

def parse_dblp(path):
    context = etree.iterparse(path, events=('end,'), tag='inproceedings')
    fast_iter(context, parse_elem)
    print len(items)

if __name__ == '__main__':
    