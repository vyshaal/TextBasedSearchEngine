import operator
import pickle
from collections import Counter
import math


class CosineSimilarity:
    def __init__(self, N, inverted_index, document_tokens):
        self.N = N
        self.inverted_index = inverted_index
        self.document_tokens = document_tokens

    def cosine_similarity_list(self, query_dict):
        ranked_list = {}
        for query_id,query in query_dict.items():
            ranked_list[query_id] = self.get_ranked_list(query)
        return ranked_list

    def get_ranked_list(self, query):
        document_scores = {}
        query_magnitude = self.calculate_query_magnitude(query)
        for doc, value in self.document_tokens.items():
            document_magnitude = self.calculate_document_magnitude(doc)
            document_scores[doc] = self.cosine_sim_value(doc, query.split(), document_magnitude, query_magnitude)
        return sorted(document_scores.items(), key=operator.itemgetter(1), reverse=True)[:100]

    def calculate_document_magnitude(self, doc):
        magnitude = 0
        token_counter = Counter(self.document_tokens[doc])
        for key, value in token_counter.items():
            doc_tf = token_counter[key] / len(self.document_tokens[doc])
            doc_idf = 1 + math.log(self.N / len(self.inverted_index[key]))
            magnitude += math.pow(doc_tf * doc_idf, 2)

        return math.sqrt(magnitude)

    def calculate_query_magnitude(self, query):
        magnitude = 0
        query_counter = Counter(query.split())
        for key, val in query_counter.items():
            query_tf = val
            query_idf = 1
            magnitude += math.pow(query_tf * query_idf, 2)
        return math.sqrt(magnitude)

    def cosine_sim_value(self, doc, query, document_magnitude, query_magnitude):
        cosine_value = 0
        token_counter = Counter(self.document_tokens[doc])
        for token in query:
            if token in self.document_tokens[doc]:
                query_tf = Counter(query)[token]
                query_idf = 1
                query_tfidf = query_tf * query_idf

                doc_tf = token_counter[token] / len(self.document_tokens[doc])
                doc_idf = 1 + math.log(self.N / len(self.inverted_index[token]))
                doc_tfidf = doc_tf * doc_idf

                cosine_value += doc_tfidf * query_tfidf

        cosine_value /= 1.0 * document_magnitude * query_magnitude
        return cosine_value


class TFIDF:
    def __init__(self, N, inverted_index, document_tokens):
        self.N = N
        self.inverted_index = inverted_index
        self.document_tokens = document_tokens

    def tf_idf_list(self, query_dict):
        ranked_list = {}
        for query_id,query in query_dict.items():
            ranked_list[query_id] = self.get_ranked_list(query)
        return ranked_list

    def get_ranked_list(self, query):
        document_scores = {}
        for key, value in self.document_tokens.items():
            document_scores[key] = self.tf_idf_value(key, query.split())
        return sorted(document_scores.items(), key=operator.itemgetter(1), reverse=True)[:100]

    def tf_idf_value(self, doc, query):
        value = 0
        token_counter = Counter(self.document_tokens[doc])
        for token in query:
            if token in self.document_tokens[doc]:

                tf = math.log(1 + token_counter[token])
                idf = 1 + math.log(self.N / len(self.inverted_index[token]))
                tfidf = tf * idf

                value += tfidf

        value /= 1.0
        return value


class BM25:
    def __init__(self, N, inverted_index, document_tokens, relevance_dict):
        self.N = N
        self.inverted_index = inverted_index
        self.document_tokens = document_tokens
        self.k1 = 1.2
        self.k2 = 100
        self.b = 0.75
        self.relevance_dict = relevance_dict
        self.avdl = self.get_avdl_value()

    def bm_25_list(self, query_dict):
        ranked_list = {}
        for query_id,query in query_dict.items():
            ranked_list[query_id] = self.get_ranked_list(query,query_id)
        return ranked_list

    def get_ranked_list(self, query, query_id):
        document_scores = {}
        for key, value in self.document_tokens.items():
            document_scores[key] = self.bm_25_value(key, query.split(), query_id)
        return sorted(document_scores.items(), key=operator.itemgetter(1), reverse=True)[:100]

    def get_k_value(self, doc):
        return self.k1 * (1 - self.b + self.b * (len(self.document_tokens[doc]) / self.avdl))

    def get_avdl_value(self):
        return sum(len(value) for key, value in self.document_tokens.items()) / self.N

    # Score is calculated using the formula

    # iΣ log[((ri + 0.5)/(R - ri + 0.5)/(ni - ri + 0.5)/(N - ni - R + ri + 0.5)) * ((k1 + 1)/(K + fi)) * ((k2 + 1)qfi/(k2+qfi))]

    #  K = k1((1-b)+b.dl/avdl)

    def bm_25_value(self, doc, query, query_id):
        value = 0
        token_counter = Counter(self.document_tokens[doc])
        k = self.get_k_value(doc)
        R = self.get_R_value(query_id)
        for token in query:
            if token in self.document_tokens[doc]:
                qfi = Counter(query)[token]
                query_factor = ((self.k2 + 1)*qfi) / (self.k2 + qfi)

                fi = token_counter[token]
                document_factor = ((self.k1 + 1)*fi) / (k + fi)

                ni = len(self.inverted_index[token])
                ri = self.get_ri_value(token,query_id)
                numerator = ((ri + 0.5) / (R - ri + 0.5))
                denominator = ((ni - ri + 0.5) / (self.N - ni - R + ri + 0.5))
                relevance_factor =  numerator/denominator
                value += math.log(relevance_factor * document_factor * query_factor)

        value /= 1.0
        return value

    def get_ri_value(self,token,query_id):
        try:
            docids = str(self.relevance_dict[query_id]).split(',')
            return sum(1 for docid in docids if token in self.document_tokens[docid])
        except KeyError:
            return 0

    def get_R_value(self,query_id):
        try:
            return str(self.relevance_dict[query_id]).count(',') + 1
        except KeyError:
            return 0