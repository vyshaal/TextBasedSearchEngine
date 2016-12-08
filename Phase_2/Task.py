import pickle
from collections import Counter
from Phase_1 import RetrievalModel
import operator

stop_words_path = "../given_files/common_words"

inverted_index = pickle.load(open("../Phase_1/inverted_index.p", "rb"))
document_tokens = pickle.load(open("../Phase_1/document_tokens.p", "rb"))
query_dict = pickle.load(open("../Phase_1/query_dict.p", "rb"))
relevance_dict = pickle.load(open("../Phase_1/relevance_dict.p", "rb"))

N = len(document_tokens)


def retrieve_docs():
    stop_words = retrieve_stop_words()
    updated_document_tokens = update_docs(stop_words)
    updated_query_dict = update_queries(stop_words)
    model = RetrievalModel.CosineSimilarity(N, inverted_index, updated_document_tokens)
    ranked_list = model.cosine_similarity_list(updated_query_dict)
    for query_id, scores in ranked_list.items():
        print(query_id + " " + query_dict[query_id])
        print(scores)
        updated_query = relevance_feedback_query(query_dict[query_id], scores, updated_document_tokens, stop_words)
        updated_list = model.cosine_similarity_list({query_id: updated_query})
        print(updated_list.values())
        break


def relevance_feedback_query(query, scores, updated_document_tokens, stop_words):
    no_of_docs = 15
    docids = [i for i, j in scores][:no_of_docs]

    all_words = []
    for docid in docids:
        all_words += updated_document_tokens[docid]

    query_term_weight = Counter(all_words)
    for query_term in query.split():
        if query_term in query_term_weight.keys():
            query_term_weight[query_term] += no_of_docs
        else:
            query_term_weight[query_term] = no_of_docs

    query_length = len(query.split())
    weighted_terms = sorted(query_term_weight.items(), key=operator.itemgetter(1), reverse=True)

    new_query = [i for i, j in weighted_terms][:query_length + 5]
    print(query)
    print(" ".join(new_query))
    return " ".join(new_query)


def retrieve_stop_words():
    stop_words = []
    with open(stop_words_path) as file:
        for line in file:
            stop_words.append(line.split()[0])

    return stop_words


def update_docs(stop_words):
    for key,values in document_tokens.items():
        document_tokens[key] = [x for x in values if x not in stop_words]

    return document_tokens


def update_queries(stop_words):
    for key,values in query_dict.items():
        query_dict[key] = " ".join([x for x in values.split() if x not in stop_words])

    return query_dict

retrieve_docs()