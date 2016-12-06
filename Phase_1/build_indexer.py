import os
from collections import Counter
import pickle
from bs4 import BeautifulSoup

inverted_index = {}
token_count = {}
document_tokens = {}

html_file_path = "../given_files/cacm/"
N = len(os.listdir(html_file_path))


def get_docID(f):
    return f.replace(".html", "")


def build_indexer():
    for file in os.listdir(html_file_path):
        if file.endswith(".html"):
            parse_text(file)


def parse_text(file):
    f = open(html_file_path + file, 'r')
    soup = BeautifulSoup(f, 'html.parser')
    content = soup.find('pre')

    unigrams = content.get_text().split()
    docid = get_docID(file)
    document_tokens[docid] = unigrams
    update_index(Counter(unigrams),docid)


def update_index(unigram_counter,docid):
    token_count[docid] = len(unigram_counter)

    for key,value in unigram_counter.items():
        try:
            inverted_index[key][docid] = value
        except KeyError:
            inverted_index[key] = {docid: value}


build_indexer()
pickle.dump(inverted_index, open("inverted_index.p", "wb"))
pickle.dump(document_tokens, open("document_tokens.p", "wb"))