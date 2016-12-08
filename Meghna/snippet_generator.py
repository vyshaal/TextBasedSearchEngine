import re


def highlight_Doc(doc, query):
    words = re.findall(r'\w+', doc)
    sequence = list(words[0])  # initializing words that represent the current snippet
    start, end = 0, 1          # initializing start(inclusive) and end(exclusive) indexes of the min snippet
    word_count = len(words)     # total word count of document
    min = word_count            # initializing the minimum word count as total word count
    snippet = (start, end)

    while end < word_count:
        if in_Snippet(sequence, query) and start < end:
            if len(sequence) < min:
                min = len(sequence)
                snippet = (start, end)
                sequence.pop(0)
                start += 1

        else:
            sequence.append(words[end])
            end += 1
    sentence = find_Sentence(doc, snippet)  # find minimal sentences that contain the snippet
    result = highlight_Sentence(sentence, query)
    return result


def in_Snippet(sequence, query):
    text = (' ').join(sequence)
    terms = query.split()
    match = True
    for term in terms:
        pattern = '(^|\s+)%s(\s+|$)' % term
        if not re.search(pattern, text, re.I):
            match = False
    return match


def find_Sentence(doc, snippet):
    pattern = re.compile(r'([^\s][^\.!?]*[\.!?])', re.M)
    sentences = pattern.finditer(doc)
    sent_indexes = [sentence.span() for sentence in sentences]
    words_match = re.finditer(r'[^\s]+(?=\s*)', doc)
    word_indexes = [word.span() for word in words_match]
    start, end = 0, 0

    while end < len(sent_indexes):
        if word_indexes[snippet[0]][0] >= sent_indexes[end][1]:
            start += 1
            end += 1
        elif word_indexes[snippet[0]][0] >= sent_indexes[start][0] and word_indexes[snippet[1]][1] <= sent_indexes[end][
            1]:
            return doc[sent_indexes[start][0]:sent_indexes[end][1]]

        elif word_indexes[snippet[0]][0] < sent_indexes[start][1] and word_indexes[snippet[1]][1] > sent_indexes[end][
            1]:
            end += 1
        else:
            pass

    return doc[sent_indexes[start][0]:sent_indexes[end][1]]


def highlight_Sentence(sentence, query):
    terms = re.sub('\s+', '|', query)
    regex = re.compile(r'(\s*)((?:\b\s*(?:%s)\b)+)' % terms, re.I)
    return regex.sub(r'\1"\2"', sentence)


if __name__ == "__main__":
    print(highlight_Doc("I like articles. Boston Globe article are fantastic.", "article are"))