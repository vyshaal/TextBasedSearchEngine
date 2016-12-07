import traceback
from math import sqrt
import os
from glob import glob
import operator

DOC_NAME ={}
QUERY_ID = 0
f = 1


def doc_vsm(query,inverted_index,N):

    try:
        query_tf = {}
        query_term = query.split()
        query_inverted_index = {}
        doc_score = {}

        for term in query_term:
            if not query_tf.has_key(term):
                query_tf.update({term:1})
            else:
                query_tf[term] = query_tf[term] + 1

        for term in query_tf:
            query_tf[term] = float(query_tf[term])/float(len(query_term))
            if inverted_index.has_key(term):
                query_inverted_index.update({term:inverted_index[term]})

            else:
                query_inverted_index.update({term:{}})

        for term in query_inverted_index:
            for docid in query_inverted_index[term]:
                if not doc_score.has_key(docid):
                    docid_score = fetch_doc_score(docid,inverted_index)
                    doc_score.update({docid: docid_score})

    except Exception as ex:
        print(traceback.format_exc())

def fetch_doc_score(docid,inverted_index)
    doc_score = 0
    for term in inverted_index:
        if inverted_index[term].has_key(docid):
            doc_score += inverted_index[term][docid]**2
    return sqrt(doc_score)


def pseudo_relevance_feedback(sorted_doc_score,query,inverted_index,N):
    global f
    relevance_index = {}
    updated_query = query
    f+= 1
    k = 10
    range_min = 10
    range_max = 20
    for i in range(0,k):
        docid,doc_score = sorted_doc_score[i]
        doc= open(DOC_NAME[docid]+".txt").read()
        for term in doc.split():
            if relevance_index.has_key(term):
                relevance_index[term] += 1
            else:
                relevance_index[term] = 1
    sorted_relevance = sorted(relevance_index.items(), key=operator.itemgetter(1), reverse=True)
    for i in range(range_min,range_max):
        term,frequency = sorted_relevance[i]
        if term not in updated_query:
            updated_query +=  " "
            updated_query +=  term

  doc_vsm(query,inverted_index,N)

def write_doc_score(sorted_doc_score):
    try:
        if(len(sorted_doc_score)>0):
            out_file  = open("VSM_Doc_Score.txt",'a')
            for i in range(min(100,len(sorted_doc_score))):
                docid,doc_score = sorted_doc_score[i]
                out_file.write(str(QUERY_ID) + " Q0 "+ DOC_NAME[docid] +"[Doc_Id = "+ str(docid)+"] " + str(i+1) + " "
                               + str(doc_score))

            out_file.write("\n")
            out_file.close()
            print ("\nDocument Scoring for Query id = " +str(QUERY_ID))
        else:
            print ("\nTerm not in the corpus")
    except Exception as e:
        print(traceback.format_exc())

def start():
    try:
        global QUERY_ID
        inverted_index,N = build_indexer()
        query_file = open("query.txt", 'r')
        for query in query_file.readlines():
            global f
            f= 1
            QUERY_ID+=1
            doc_vsm(query,inverted_index,N)
    except Exception as e:
        print(traceback.format_exc())

start()
