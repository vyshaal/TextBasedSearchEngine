import os
from collections import Counter
import pickle
from bs4 import BeautifulSoup
from math import log
import traceback

inverted_index = {}
token_count = {}
document_tokens = {}
DOC_NAME ={}
QUERY_ID = 0
stopwords = []
counter = 1

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
    document_tokens[docid] = filter_words(unigrams,docid)
    update_index(Counter(document_tokens[docid]),docid)

    with open('common_words') as f:
        stopwords = f.read().splitlines()
    for term in doc.split():
        if term not in stopwords:
            if not inverted_index.has_key(term):
                doc_term_freq = {docid: 1}
                inverted_index.update({term: doc_term_freq})
            elif not inverted_index[term].has_key(docid):
                inverted_index[term].update({docid: 1})
            else:
                inverted_index[term][docid] += 1
                counter += 1
                N = counter - 1
    for term in inverted_index:
        idf = 1.0 + log(float(N) / float(
        len(inverted_index[term].keys()) + 1))
    for doc in inverted_index[term]:
        normalized_tf = float(inverted_index[term][doc]) / float(
            document_tokens[doc])
        inverted_index[term][doc] = normalized_tf * idf
        print(traceback.format_exc())
        return inverted_index,N


def update_index(unigram_counter,docid):
    token_count[docid] = len(unigram_counter)

    for key,value in unigram_counter.items():
        try:
            inverted_index[key][docid] = value
        except KeyError:
            inverted_index[key] = {docid: value}


def filter_words(unigrams,docid):
    index = [i for i in range(len(unigrams)) if "PM" in unigrams[i] or "AM" in unigrams[i]][-1]
    filtered_words = unigrams[:index+1]
    return clean_content(" ".join(filtered_words)).split()


def clean_content(s):
    s = s.replace('-',' ').lower()
    return ''.join(e for e in s if e.isalnum() or e == " ")


build_indexer()
pickle.dump(inverted_index, open("inverted_index.p", "wb"))
pickle.dump(document_tokens, open("document_tokens.p", "wb"))