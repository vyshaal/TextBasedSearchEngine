from stemming.porter2 import stem
import string
import pickle

"""
    Snippet Generator:
        Highlights the query terms in the document for a given doc id
"""


class SnippetGenerator:

    # initialize with document tokens, path of stop words
    def __init__(self, document_tokens, stop_words_path = ""):
        self.document_tokens = document_tokens
        self.stop_words = self.retrieve_stop_words(stop_words_path)

    # convert each document to list of dictionary tokens
    def doc_to_tokens(self, doc):
        tokens = []
        doc = doc.split(' ')
        for x in range(len(doc)):
            token = dict()
            token['original'] = doc[x]
            token['stemmed'] = stem(''.join(ch for ch in doc[x] if ch not in string.punctuation).lower())
            token['stemmed'] = stem(doc[x])
            token['op'] = len(' '.join(doc[:x + 1])) - len(doc[x])
            tokens.append(token)
        return tokens

    # returns back the original doc
    def build_doc_from_tokens(self, token_list):
        result = ''
        for x in range(len(token_list)):
            result = ' '.join([result, token_list[x]['original']])
        return result.strip()

    # add neighbouring terms to the key words
    def add_from_surround(self, doc_tokens, query_tokens):
        doc = self.build_doc_from_tokens(doc_tokens)
        if len(doc) < 200:
            return [doc]
        surround_tokens = []
        keyword_sp = []
        query_token = query_tokens[0]
        for query_token in query_tokens:
            for doc_token in doc_tokens:
                if query_token['stemmed'] == doc_token['stemmed']:
                    keyword_sp.append((doc_token['op'], doc_token['original']))

        if keyword_sp == []:
            return [doc[200:]]

        for x in range(len(keyword_sp)):
            surround_tokens.append(self.extract_surround(doc, keyword_sp[x][0], True, True))
            surround_tokens.append(self.extract_surround(doc, keyword_sp[x][0] + 200 / 2, False, True))
            surround_tokens.append(self.extract_surround(doc, keyword_sp[x][0] + len(keyword_sp[x][1]) - 200 / 2,
                                                         True, False))

        return surround_tokens

    # returns the neighbouring terms
    def extract_surround(self, doc, index, flag_left, flag_right):
        left = int(max(index - 200 / 2, 0))
        right = int(min(index + 200 / 2, len(doc)))
        if right == len(doc):
            flag_right = False
        if left == 0:
            flag_left = False

        leftpf = False
        if flag_left and doc[left - 1].isalnum() and doc[left].isalnum():
            x = left
            while doc[x] != ' ':
                x += 1
            if x - left >= 4:
                leftpf = True
            left = x

        rightpf = False
        if flag_right and doc[right].isalnum() and doc[right - 1].isalnum():
            y = right
            while doc[y] != ' ':
                y -= 1
            if right - y >= 4:
                rightpf = True
            right = y

        surround = (doc[left:right]).strip()
        if leftpf:
            surround = "".join(['... ', surround])
        if rightpf:
            surround = "".join([surround, ' ...'])
        return surround

    # returns snippet score
    def calculate_snippet_score(self, surrounds, doc_tokens, query_tokens):
        max_score = -1
        for surround in surrounds:
            surround_token_list = self.doc_to_tokens(surround)
            score = 0
            for query_token in query_tokens:
                for surround_token in surround_token_list:
                    if query_token['stemmed'] == surround_token['stemmed']:
                        doc_count = 0
                        for doc_token in doc_tokens:
                            if doc_token['stemmed'] == query_token['stemmed']:
                                doc_count += 1

                        score += 1. / doc_count

            if score > max_score:
                max_score = score
                best_surround_tokens = surround_token_list

        return best_surround_tokens

    # highlight query terms in a doc
    def highlight_document(self, best_surround_tokens, query_tokens):
        snippet_text = ''
        query_tokenized = self.build_doc_from_tokens(query_tokens)
        for surround_token in best_surround_tokens:
            if surround_token['stemmed'] in query_tokenized.split():
                snippet_text = ' '.join([snippet_text, '"'])
                snippet_text = ''.join([snippet_text, surround_token['original']])
                snippet_text = ''.join([snippet_text, '"'])
            else:
                snippet_text = ' '.join([snippet_text, surround_token['original']])
        return snippet_text.replace('" "', ' ').strip()

    # generate a snippet for a given docid and a query
    def generate_snippet(self, docid, query):
        doc_tokens = self.doc_to_tokens(" ".join(self.document_tokens[docid]))
        query_tokens = self.doc_to_tokens(self.clean(query))
        surrounds = self.add_from_surround(doc_tokens, query_tokens)
        best_surround_tokens = self.calculate_snippet_score(surrounds, doc_tokens, query_tokens)
        return self.highlight_document(best_surround_tokens, query_tokens)

    # retrieve stop words
    def retrieve_stop_words(self, stop_words_path):
        stop_words = []
        if stop_words_path == "":
            return stop_words
        with open(stop_words_path) as file:
            for line in file:
                stop_words.append(line.split()[0])
        return stop_words

    # clean query from stop words
    def clean(self,query):
        query_list = query.split(" ")
        return " ".join([term for term in query_list if term not in self.stop_words])