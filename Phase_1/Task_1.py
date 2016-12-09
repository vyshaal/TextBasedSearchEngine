import pickle
import operator
from collections import Counter
import os
import math
from Phase_1 import RetrievalModel
import csv

inverted_index = pickle.load(open("inverted_index.p", "rb"))
document_tokens = pickle.load(open("document_tokens.p", "rb"))
query_dict = pickle.load(open("query_dict.p", "rb"))
relevance_dict = pickle.load(open("relevance_dict.p", "rb"))

vsm_table = "vsm.csv"
tfidf_table = "tfidf.csv"
bm25_table = "bm25.csv"

N = len(document_tokens)

query_file_path = "../given_files/"
query_file = open(query_file_path + "cacm.query","rb")
dict = {}


def retrieve_relevant_documents():
    retrieve_cosine_sim_docs()
    retrieve_tf_idf__docs()
    retrieve_bm_25_docs()


def retrieve_cosine_sim_docs():
    cosine_sim = RetrievalModel.CosineSimilarity(N, inverted_index, document_tokens)
    ranked_list = cosine_sim.cosine_similarity_list(query_dict)

    with open(vsm_table, "w") as file:
        csv_writer = csv.writer(file)
        for query_id, scores in ranked_list.items():
            i = 0
            for score in scores:
                i += 1
                csv_writer.writerow((query_id, "Q0", score[0], i, score[1], "vector_space_model"))
#                print(query_id,query_dict[query_id])
#                print(score)
    file.close()


def retrieve_tf_idf__docs():
    tf_idf = RetrievalModel.TFIDF(N, inverted_index, document_tokens)
    ranked_list = tf_idf.tf_idf_list(query_dict)

    with open(tfidf_table, "w") as file:
        csv_writer = csv.writer(file)
        for query_id, scores in ranked_list.items():
            i = 0
            for score in scores:
                i += 1
                csv_writer.writerow((query_id, "Q0", score[0], i, score[1], "tf_idf"))
#                print(query_id,query_dict[query_id])
#                print(score)
    file.close()


def retrieve_bm_25_docs():
    bm_25 = RetrievalModel.BM25(N, inverted_index, document_tokens, relevance_dict)
    ranked_list = bm_25.bm_25_list(query_dict)

    with open(bm25_table, "w") as file:
        csv_writer = csv.writer(file)
        for query_id, scores in ranked_list.items():
            i = 0
            for score in scores:
                i += 1
                csv_writer.writerow((query_id, "Q0", score[0], i, score[1], "bm_25"))
#                print(query_id,query_dict[query_id])
#                print(score)
    file.close()

retrieve_relevant_documents()