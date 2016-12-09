import operator
import re
import sys
from optparse import OptionParser

query_term = ""
doc_content = []
doc_content = open("document_tokens.p",'r')
snippet_keyword = query_term
PUNCTUATION = set(('.', '?', '!', '...'))
SUGGESTIONS = set("""

    """.split()) #include highly ranked terms from documents

lookahead = 10  # Number of tokens to show before snippet_keyword

tokens = doc_content.split(" ")  # Split string into a list of tokens or use document_tokens file

found_index = -1  #  Represents the index of the token.  Initialize to -1 and assume it doesn't exist.

# Loop through tokens and compare each to the snippet_keyword.  If we find the snippet_keyword, rememeber the index and break out of the loop

found_index = tokens.index(snippet_keyword)

try:
    found_index = tokens.index(snippet_keyword)
    # Get the max of the found index minus the number of words to show before the snippet_keyword, and 0
    found_index = max(found_index - lookahead, 0)

    # Create a sub list of the tokens from the found_index and end, then join those terms back together with a space.
    snippet = " ".join(tokens[found_index:len(tokens)])

except ValueError:
    snippet = ""  # No snippet or whatever error handling you are going to do

print (snippet)
#######################################################################
def highlighter(doc,query,snippet_char,snippet_sentence):
    sentences = [split_into_word(sent) for sent in split_into_sentences(doc)]
    query = split_into_word(query)

    snippet_sentences = select_snippet_sentences(sentences, query , snippet_char, snippet_sentence)
    snippet_words = []

    for sent in snippet_sentences:
        snippet_words += sent

        highlighted_snippet = insert_highlights(snippet_words,query)

        if not highlighted_snippet:
            return ''
        else:
            return join_words(highlighted_snippet)

def insert_highlights(snippet_words, query_words):

            span = dict(find_query_span(snippet_words,query_words))
            strings =[]
            i=0

            while i<len(snippet_words):
                if span.has_key(i):
                    start,end =i,span[i]
                    strings.append("'")
                    strings.extend(snippet_words[start: end])
                    strings.append("'")
                    i=end

                else :
                    strings.append(snippet_words[i])
                    i +=1
                    return strings

def select_snippet_sentences(sentences,query_words,snippet_char,snippet_sentence):
    ranked_sentences = [(pos, sent, score) for (pos, (sent, score))
                        in enumerate(rank_sentences(sentences, query_words))]

    ranked_sentences.sort(key=operator.itemgetter(2), reverse=True)

    char_count = sent_count = 0
    keep = []
    for (pos, sentence, score) in ranked_sentences:
        length = len(''.join(insert_highlights(sentence, query_words)))

        if char_count + length > snippet_char or sent_count + 1 > snippet_sentence:
            continue
        else:
            keep.append((pos, sentence, score))
            char_count += length
            sent_count += 1

    keep.sort(key=operator.itemgetter(0))


    positive_scores = [triplet for triplet in keep if triplet[2] > 0]
    if positive_scores:
        return [triplet[1] for triplet in positive_scores]
    else:
        return [triplet[1] for triplet in keep]


def rank_sentences(sentences, query_words):

    scores = []
    for sentence in sentences:
        score = score_sentence(sentence, query_words)
        scores.append((sentence, score))

    return scores

def count_suggestions(sentence):
    return sum(1 for word in sentence if word in SUGGESTIONS)


def score_sentence(sentence, query_words):
    opinion_indicator_count = count_suggestions(sentence)
    query_match_score = query_match_score (sentence, query_words)
    return opinion_indicator_count + query_match_score


def query_match_score(sentence, query_words):
    spans = find_query_span(sentence, query_words)
    return sum((span[1] - span[0]) ** 2 for span in spans)


def find_query_span(words, query_words):

    spans = []
    in_span = False
    old_query_index = None
    span_start = None


    words = [word.lower() for word in words]
    query_words = [query_word.lower() for query_word in query_words]

    for i, word in enumerate(words):
        if word in query_words:
            query_index = query_words.index(word)

            if in_span:
                if old_query_index + 1 != query_index:

                    span_end = i
                    spans.append((span_start, span_end))
                    span_start = i
            else:

                in_span = True
                span_start = i
            old_query_index = query_index

        elif word not in query_words and in_span:

            in_span = False
            span_end = i
            spans.append((span_start, span_end))

    if in_span:

        spans.append((span_start, len(words)))

    return spans


def join_words(words):

    strings = []
    for i, word in enumerate(words[: -1]):
        if i + 1 < len(words) and words[i + 1] in PUNCTUATION:
            strings.append(word)
        elif word == '""':
            strings.append(word)
        elif i + 1 < len(words) and words[i + 1] == '""':
            strings.append(word)
        else:
            strings.append(word + ' ')
    return ''.join(strings) + words[-1]


def split_into_sentences(doc):

    doc = re.sub(r'\s+', ' ', doc)
    pat = re.compile(r"""([A-Za-z0-9 ,'"@#$%^&*()~=+-]+(\.{3}|[.?!]))""")
    sentences = [sent[0].strip() for sent in pat.findall(doc)]


    if not sentences:
        return [doc]
    else:
        return sentences


def split_into_word(sentence):

    pat = re.compile(r"""
                ['"]?[-A-Za-z0-9@#$%^&*()'~=+_-]+['"]?
                |
                ,
                |
                \.{3}
                |
                [.?!]
                """, re.VERBOSE)
    return pat.findall(sentence)


def main(args):


    description = 'Command-line interface to the snippet maker.'
    usage = '%prog <DOCUMENT> <QUERY_STRING> [options]'
    parser = OptionParser(usage=usage, description=description)

    parser.add_option('-c', '--chars', dest='snippet_char',
                      help='The maximum number of characters to include in the snippet.')

    parser.add_option('-s', '--sents', dest='snippet_sentence',
                      help='The maximum number of sentences to include in the snippet.')

    options, args = parser.parse_args(args)

    if len(args) != 2:
        parser.error('Incorrect number of arguments.')
    doc = args[0]
    query = args[1]

    snippet = highlighter(doc, query, options.snippet_char, options.snippet_sentence)
    print
    snippet
    return 0


if __name__ == '__main__':
    exit(main(sys.argv[1:]))





