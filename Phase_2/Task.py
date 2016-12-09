import pickle
from collections import Counter
from Phase_1 import RetrievalModel
import operator
import csv
from Phase_1 import Snippet

"""
Generates ranked lists (in descending order) for all the given 64 queries using query expansion technique and Stopping

Note: Vector space model is used for retrieving the documents
      Psuedo relevance feedback for query expansion
"""

stop_words_path = "../given_files/common_words"

inverted_index = pickle.load(open("../Phase_1/inverted_index.p", "rb"))
document_tokens = pickle.load(open("../Phase_1/document_tokens.p", "rb"))
query_dict = pickle.load(open("../Phase_1/query_dict.p", "rb"))
relevance_dict = pickle.load(open("../Phase_1/relevance_dict.p", "rb"))

N = len(document_tokens)

query_expansion_stopping_table = "query_expansion_with_stopping_vsm.csv"


# retrieve documents using query expansion and stopping techniques
def retrieve_docs():
    snippet_generator = Snippet.SnippetGenerator(document_tokens, "")
    stop_words = retrieve_stop_words()
    updated_document_tokens = update_docs(stop_words)
    updated_query_dict = update_queries(stop_words)
    model = RetrievalModel.CosineSimilarity(N, inverted_index, updated_document_tokens)
    ranked_list = model.cosine_similarity_list(updated_query_dict)

    with open(query_expansion_stopping_table, "w") as file:
        csv_writer = csv.writer(file)
        new_query_dict = {}
        for query_id, scores in ranked_list.items():
            updated_query = relevance_feedback_query(query_dict[query_id],scores, updated_document_tokens)
            new_query_dict[query_id] = updated_query

        updated_list = model.cosine_similarity_list(new_query_dict)
        for query_id, scores in updated_list.items():
            i = 0
            for score in scores:
                i += 1
                csv_writer.writerow((query_id, "Q0", score[0], i, score[1], "query_expansion_with_stopping"))
                if i == 1:
                    query = query_dict[query_id]
                    print("Given Query: " + query)
                    print("Top Document for given query: " + score[0])
                    print("Snippet: \n" + snippet_generator.generate_snippet(score[0],query))
    file.close()


# returns a new query after psuedo relevance feedback (after updating new weights)
def relevance_feedback_query(query, scores, updated_document_tokens):
    no_of_docs = 12
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

    new_query = [i for i, j in weighted_terms][:query_length]
    return " ".join(new_query)


# retrieve stop words
def retrieve_stop_words():
    stop_words = []
    with open(stop_words_path) as file:
        for line in file:
            stop_words.append(line.split()[0])

    return stop_words


# cleans corpus from the stop words
def update_docs(stop_words):
    for key,values in document_tokens.items():
        document_tokens[key] = [x for x in values if x not in stop_words]

    return document_tokens


# cleans queries from the stop words
def update_queries(stop_words):
    for key,values in query_dict.items():
        query_dict[key] = " ".join([x for x in values.split() if x not in stop_words])

    return query_dict

retrieve_docs()