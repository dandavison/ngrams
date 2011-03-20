# import the os module
import os

# extra modules
import codecs

import rdflib


def write_gutenberg_data_rdf():
    graph = rdflib.Graph()
    rdf = graph.parse(fd, format="application/rdf+xml")


from lxml.etree import iterparse

def get_dc_element(el, el_name):
    elements = list(el.iterfind('{http://purl.org/dc/elements/1.1/}' + el_name))
    if len(elements) == 1:
        return elements[0]
    else:
        return None

def write_gutenberg_data_iterparse(infile, outfile):
    out_fd = codecs.open(outfile, 'w', 'utf-8')
    in_fd = open(infile, 'r')

    for el in iterparse(in_fd):

        assert el[0] =='end', (el,)
        el = el[1]

        if el.tag != '{http://www.gutenberg.org/rdfterms/}etext':
            continue

        creator = get_dc_element(el, 'creator')
        if creator is None:
            continue

        # etext id
        try:
            etext_id = el.values()[0].replace('etext', '')
            etext_id = int(etext_id)
        except:
            print etext_id
            print 'Error parsing etext id'
            raise

        # author, dates
        birth_year, death_year = '', ''
        if len(creator.text.split(', ')) >= 2:
            years = creator.text.split(', ')[-1].split('-')
            try:
                birth_year, death_year = map(int, years)
            except:
                # Could not determine years; skip
                continue

        title = get_dc_element(el, 'title')

        url = 'http://www.gutenberg.org/cache/epub/%s/pg%s.txt' % (
            etext_id, etext_id)

        if 1730 < birth_year < 1885 and \
           1800 < death_year < 2000:

            fields = [creator.text,
                      birth_year,
                      death_year,
                      title.text if title is not None else '',
                      url]

            row = '\t'.join(map(unicode, fields)).replace('\n', '')
            out_fd.write(row + '\n')

    in_fd.close()
    out_fd.close()


# This version uses a more basic XML library but it involves reading
# the entire XML file into memory which requires a very large amount
# of RAM for large XML files (e.g. the gutenberge catalog is 193M and
# required > 8Gb RAM to load into memory in python as parsed XML)

# import the python module that will parse the XML input file
from xml.dom import minidom

def write_gutenberg_data(gut):
    outfile = codecs.open('gutenberg_data.txt', 'w', 'utf-8')

    for element in gut.getElementsByTagName('pgterms:etext'):
        creator_elements = element.getElementsByTagName('dc:creator')
        if len(creator_elements) == 0:
            continue
        assert len(creator_elements) == 1, 'Should only be one creator!'
        creator_el = creator_elements[0]
        children = creator_el.childNodes
        # assert len(children) == 1, 'Should only be one child!'

        creator_text = ''
        for child in children:
            try:
                 creator_text += child.data
            except:
                pass

        if len(creator_text.split(', ')) >= 2:
            years = creator_text.split(', ')[-1].split('-')
            try:
                birth_year, death_year = map(str, map(int, years))
            except:
                birth_year, death_year = '', ''

        title = element.getElementsByTagName('dc:title')[0].childNodes[0].data
        etext_num = element.getAttribute('rdf:ID').replace('etext', '')
        url = 'http://www.gutenberg.org/cache/epub/%s/pg%s.txt' % (etext_num, etext_num)
        fields = [creator_text, birth_year, death_year, title, url]
        row = '\t'.join(fields).replace('\n', '')
        outfile.write(row + '\n')


if __name__ == '__main__':
    # store the location of your input file in a variable
    infile = '/Users/Shared/Mary/Gutenberg/catalog.rdf'

    # parse the XML in that file into a python data structure
    # We'd like to just do this:
    # gut = minidom.parse(file_path)
    # But that reads the whole thing into memory, and the file is too big for that. So we have to use the bufsize argument:
    gut = minidom.parse(file_path, parser=None, bufsize=1)
