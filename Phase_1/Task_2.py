import pickle
from collections import Counter
from Phase_1 import RetrievalModel
import operator

inverted_index = pickle.load(open("inverted_index.p", "rb"))
document_tokens = pickle.load(open("document_tokens.p", "rb"))
query_dict = pickle.load(open("query_dict.p", "rb"))
relevance_dict = pickle.load(open("relevance_dict.p", "rb"))

N = len(document_tokens)


def retrieve_bm_25_docs():
    bm_25 = RetrievalModel.BM25(N, inverted_index, document_tokens, relevance_dict)
    ranked_list = bm_25.bm_25_list(query_dict)
    for query, scores in ranked_list.items():
        relevance_feedback(query,scores)
        break


def relevance_feedback(query,scores):
    docids = [i for i,j in scores][:5]
    print(docids)
    all_words = []
    for docid in docids:
        all_words += document_tokens[docid]
    high_freq_words_dict = Counter(all_words)
    sorted_list = sorted(high_freq_words_dict.items(), key=operator.itemgetter(1), reverse=True)
    add_terms = [i for i,j in sorted_list][:30]
    freq_terms = [j for i, j in sorted_list][:30]

    print(add_terms)
    print(freq_terms)

retrieve_bm_25_docs()