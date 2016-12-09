The tools used are Python 3.4.0, Pycharm 

packages that were imported are:

-- BeautifulSoup from BS4
-- stem from stemming.porter2
-- Counter from Collections
-- os
-- math
-- operator
-- pickle
-- csv

-------------------------------------------------------------------

Files Submitted and their Description:

------------Files in folder Phase_1--------------:

-- The files build_indexer.py, relevance_values.py, read_queries.py are used to create pickle files to maintain document_tokens (holds the cleaned list of tokens in that document), inverted_index (consists of inverted index of the corpus), relevance_dict (which has the query id and its respective comma separated values of Doc_ids) and query_dict(which has the query_id and the list of tokens of that query) values as pickle files which are accessed in other files while calculating the document scores.

-- RetrievalModel.py holds the classes (CosineSimilarity, TFIDF, BM25) for the different retrieval models.

-- snippet.py has the snippet generator class to generate the snippet code.

-- Task_1.py when run generates 3 csv files which has tables for tf-idf, vector space model and bm25 results for retrieved documents. The tables are in the document tfidf.csv, vsm.csv and bm25.csv respectively. The table is in the format: Query_ID Q0 Doc_ID Rank Score Model_name

-- Task_2.py when run generates 1 csv file which has the table for query_expansion results for retrieved documents. The table is in the document query_expansion.csv The table is in the format: Query_ID Q0 Doc_ID Rank Score Model_name

-- Task_3A.py when run generates 1 csv file which has the table for stopping technique results for retrieved documents. The table is in the document stopping_vsm.csv The table is in the format: Query_ID Q0 Doc_ID Rank Score Model_name

-- Task_3B.py when run generates 1 csv file which has the table for stopping technique results for retrieved documents. The table is in the document stopping_vsm.csv The table is in the format: Query_ID Q0 Doc_ID Rank Score Model_name


------------Files in folder Phase_2---------------:


-- Task.py when run generates 1 csv file which has table for query expansion technique results after removing stop words. The table is the document query_expansion_with_stopping_vsm.csv is in the format:  Query_ID Q0 Doc_ID Rank Score Model_name

-- Retrieval_effectiveness.py when run generates 

1) 40 csv files which has tables for Precision and Recall, MAP, MRR, P@K K = 5 and 20 in the folder performance_acessment which is inside Phase_2 folder

2) 8 image files for graphs for all the 8 runs depicting the precision vs recall graph which are in the folder Plots inside the folder Phase_2.

Files in performance_acessment folder:

bm25_MAP.csv	
bm25_MRR.csv	
bm25_P@K=20.csv
bm25_P@K=5.csv	
bm25_Precision&Recall.csv	
lucene_MRR.csv	
lucene_P@K=20.csv
lucene_P@K=5.csv	
lucene_Precision&Recall.csv	
query_expansion_MAP.csv	
query_expansion_MRR.csv	
query_expansion_P@K=20.csv	
query_expansion_P@K=5.csv	
query_expansion_Precision&Recall.csv	
query_expansion_with_stopping_MAP.csv	
query_expansion_with_stopping_MRR.csv	
query_expansion_with_stopping_P@K=20.csv	
query_expansion_with_stopping_P@K=5.csv	
query_expansion_with_stopping_Precision&Recall.csv	
stemming_MAP.csv	
stemming_MRR.csv	
stemming_P@K=20.csv	
stemming_P@K=5.csv	
stemming_Precision&Recall.csv	
stopping_MAP.csv	
stopping_MRR.csv	
stopping_P@K=20.csv	
stopping_P@K=5.csv	
stopping_Precision&Recall.csv	
tfidf_MAP.csv	
tfidf_MRR.csv	
tfidf_P@K=20.csv	
tfidf_P@K=5.csv	
tfidf_Precision&Recall.csv	
vsm_MRR.csv	
vsm_P@K=20.csv	
vsm_P@K=5.csv	
vsm_Precision&Recall.csv

Files in Plots folder:

bm25.png	
lucene.png	
query_expansion.png
query_expansion_with_stopping.png	
stemming.png	
stopping.png	
tfidf.png
vsm.png

--------------------------------------------

----PHASE-1----

Task 1.

Steps to run the code.

1) Open the zip file Project and extract the files to the desired location.
2) Open the extracted files and in that open Phase_1 folder
3) Run the Task_1.py file using the command "python Task_1.py" in the interpreter

Task 2.

Steps to run the code.

1) Open the zip file Project and extract the files to the desired location.
2) Open the extracted files and in that open Phase_1 folder
3) Run the Task_2.py file using the command "python Task_2.py" in the interpreter

Task 3A.

Steps to run the code.

1) Open the zip file Project and extract the files to the desired location.
2) Open the extracted files and in that open Phase_1 folder
3) Run the Task_3A.py file using the command "python Task_2.py" in the interpreter

Task 3B.

Steps to run the code.

1) Open the zip file Project and extract the files to the desired location.
2) Open the extracted files and in that open Phase_1 folder
3) Run the Task_3B.py file using the command "python Task_2.py" in the interpreter

----------------------------------------

----PHASE-2----

7th run. Query expansion combined with Stopping:

Steps to run the code.

1) Open the zip file Project and extract the files to the desired location.
2) Open the extracted files and in that open Phase_2 folder
3) Run the Task.py file using the command "python Task.py" in the interpreter

Calculating MAP, MRR, P@k for k = 5 and 20, Precision and Recall:

Steps to run the code.

1) Open the zip file Project and extract the files to the desired location.
2) Open the extracted files and in that open Phase_2 folder
3) Run the retrieval_effectiveness.py file using the command "python retrieval_effectiveness.py" in the interpreter


--------------------------------------- 

Lucene:

-- HW4.java contains the lucene code for TASK-1.
-- Configure the jar files from src/java_jar/
-- When run created index is in lucene/index, provide corpus -> ../given_files/cacm and output table is the document Lucene.csv (in Phase_1
   in the format Query_ID Q0 Doc_ID Rank Score Model_name.