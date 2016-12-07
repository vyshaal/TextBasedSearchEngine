import re
import pickle
import string

query_file_path = "../given_files/cacm.query"
query_dict = {}


def clean_content(s):
    s = s.replace('-',' ').lower()
    return ''.join(e for e in s if e.isalnum() or e == " ")


def read_queries():
    queries = {}
    with open(query_file_path) as content:
        regex = re.compile(r'<DOCNO>\s+(.*?)\s+</DOCNO>(.*?)</DOC>',re.DOTALL)
        queries = re.findall(regex, content.read().replace('\n',' '))

    for query_id,query in queries:
        query_dict[query_id] = clean_content(query)

#    print(query_dict)
    pickle.dump(query_dict, open("query_dict.p", "wb"))

read_queries()