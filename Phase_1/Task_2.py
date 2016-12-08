import pickle
from collections import Counter
from Phase_1 import RetrievalModel
import operator

inverted_index = pickle.load(open("inverted_index.p", "rb"))
document_tokens = pickle.load(open("document_tokens.p", "rb"))
query_dict = pickle.load(open("query_dict.p", "rb"))
relevance_dict = pickle.load(open("relevance_dict.p", "rb"))

N = len(document_tokens)


def retrieve_docs():
    model = RetrievalModel.CosineSimilarity(N, inverted_index, document_tokens)
    ranked_list = model.cosine_similarity_list(query_dict)
    for query_id, scores in ranked_list.items():
        print(query_id + " " + query_dict[query_id])
        print(scores)
        updated_query = relevance_feedback_query(query_dict[query_id],scores)
        updated_list = model.cosine_similarity_list({query_id : updated_query})
        print(updated_list.values())
        break


def relevance_feedback_query(query,scores):
    no_of_docs = 5
    docids = [i for i,j in scores][:no_of_docs]

    all_words = []
    for docid in docids:
        all_words += document_tokens[docid]

    query_term_weight = Counter(all_words)
    for query_term in query.split():
        if query_term in query_term_weight.keys():
            query_term_weight[query_term] += no_of_docs
        else:
            query_term_weight[query_term] = no_of_docs

    query_length = len(query.split())
    weighted_terms = sorted(query_term_weight.items(), key=operator.itemgetter(1), reverse=True)

    new_query = [i for i, j in weighted_terms][:query_length+20]
    return " ".join(new_query)

retrieve_docs()