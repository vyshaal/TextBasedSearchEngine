import re
import pickle

query_file_path = "../given_files/cacm.query"
query_dict = {}


def read_queries():
    queries = {}
    with open(query_file_path) as content:
        regex = re.compile(r'<DOCNO>\s+(.*?)\s+</DOCNO>(.*?)</DOC>',re.DOTALL)
        queries = re.findall(regex,content.read().replace("\n", ''))

    for query_number,query in queries:
        query_dict[query_number] = query

    print(query_dict)
    pickle.dump(query_dict, open("query_dict.p", "wb"))

read_queries()