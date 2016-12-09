import pickle
from collections import Counter
from Phase_1 import RetrievalModel
import operator
import csv

stem_table = "stemming_vsm.csv"

stem_query_path = "../given_files/cacm_stem.query.txt"
stem_corpus_path = "../given_files/cacm_stem.txt"


def retrieve_docs():
    document_tokens = token_index()
    stem_query_dict = retrieve_query()
    inverted_index = build_index(document_tokens)
    model = RetrievalModel.CosineSimilarity(len(document_tokens), inverted_index, document_tokens)
    ranked_list = model.cosine_similarity_list(stem_query_dict)

    with open(stem_table, "w") as file:
        csv_writer = csv.writer(file)
        for query_id, scores in ranked_list.items():
            i = 0
            for score in scores:
                i += 1
                csv_writer.writerow((query_id, "Q0", score[0], i, score[1], "using_stemmed_words"))
    file.close()


def retrieve_query():
    query_dict = {}
    i = 1
    with open(stem_query_path) as file:
        for line in file:
            query_dict[str(i)] = " ".join(line.split())
            i += 1
    return query_dict


def token_index():
    document_tokens ={}
    tokens = ""
    with open(stem_corpus_path) as file:
        for line in file:
            tokens += ' '.join(line.split()) + " "

        doc_list = tokens.split('#')
        for doc in doc_list[1:]:
            all_tokens = doc.split()
            doc_id = all_tokens[0]
            tokens = all_tokens[1:]
            if "pm" in tokens:
                index = tokens.index("pm")
            elif "am" in tokens:
                index = tokens.index("am")
            else:
                index = [tokens.index(token) for token in tokens if "pm" in token][-1]
            document_tokens[retrieve_appropriate_docid(doc_id)] = tokens[:index+1]
    return document_tokens


def build_index(document_tokens):
    inverted_index = {}
    for doc_id,tokens in document_tokens.items():
        unigram_counter = Counter(document_tokens[doc_id])
        for key, value in unigram_counter.items():
            try:
                inverted_index[key][doc_id] = value
            except KeyError:
                inverted_index[key] = {doc_id: value}

    return inverted_index


def retrieve_appropriate_docid(s):
    s = "CACM-" + s
    while len(s) < 9:
        s = s.replace("-","-0")
    return s

retrieve_docs()