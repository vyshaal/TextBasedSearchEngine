import pickle
from collections import Counter
from Phase_1 import RetrievalModel
import operator
import csv
from Phase_1 import Snippet

"""
Generates ranked lists (in descending order) for all the given 64 queries using query expansion technique

Note: Vector space model is used for retrieving the documents
      Psuedo relevance feedback for query expansion
"""

inverted_index = pickle.load(open("inverted_index.p", "rb"))
document_tokens = pickle.load(open("document_tokens.p", "rb"))
query_dict = pickle.load(open("query_dict.p", "rb"))
relevance_dict = pickle.load(open("relevance_dict.p", "rb"))

N = len(document_tokens)
query_expansion_table = "query_expansion.csv"
stop_words_path = "../given_files/common_words"


# retrieves ranked lists generated using query expansion technique
def retrieve_docs():
    snippet_generator = Snippet.SnippetGenerator(document_tokens,stop_words_path)
    model = RetrievalModel.CosineSimilarity(N, inverted_index, document_tokens)
    ranked_list = model.cosine_similarity_list(query_dict)
    with open(query_expansion_table, "w") as file:
        csv_writer = csv.writer(file)
        updated_query_dict = {}
        for query_id, scores in ranked_list.items():
            updated_query = relevance_feedback_query(query_dict[query_id],scores)
            updated_query_dict[query_id] = updated_query

        updated_list = model.cosine_similarity_list(updated_query_dict)
        for query_id, scores in updated_list.items():
            i = 0
            for score in scores:
                i += 1
                csv_writer.writerow((query_id, "Q0", score[0], i, score[1], "query_expansion"))
                if i == 1:
                    query = query_dict[query_id]
                    print("Given Query: " + query)
                    print("Top Document for given query: " + score[0])
                    print("Snippet: \n" + snippet_generator.generate_snippet(score[0],query))
    file.close()


# returns updated query after psuedo_relevance_feedback
def relevance_feedback_query(query,scores):
    no_of_docs = 12
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

    new_query = [i for i, j in weighted_terms][:query_length+5]
    return " ".join(new_query)

retrieve_docs()