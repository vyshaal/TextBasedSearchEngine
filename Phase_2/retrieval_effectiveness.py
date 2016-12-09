import csv
import pickle
import matplotlib.pyplot as plt

relevance_dict = pickle.load(open("../Phase_1/relevance_dict.p", "rb"))

vsm_file = open("../Phase_1/vsm.csv")
bm25_file = open("../Phase_1/bm25.csv")
tfidf_file = open("../Phase_1/tfidf.csv")
lucene_file = open("../Phase_1/Lucene.csv")
query_expansion_file = open("../Phase_1/query_expansion.csv")
stemming_file = open("../Phase_1/stemming_vsm.csv")
stopping_file = open("../Phase_1/stopping_vsm.csv")
query_expansion_with_stopping_file = open('query_expansion_with_stopping_vsm.csv')
dir = "performance_acessment/"
plots = "plots/"


def calculate_effectiveness(file,name):
    csv_reader = csv.reader(file)
    query_dict = {}
    for row in csv_reader:
        try:
            query_dict[row[0]] += [row[2]]
        except KeyError:
            query_dict[row[0]] = [row[2]]

    print(len(query_dict))
    reciprocal_rank = []
    average_precision_list = []
    precision_at_5 = []
    precision_at_20 = []
    precision_dict = {}
    recall_dict = {}

    for query_id,docs in query_dict.items():
        average_precision = 0
        if query_id in relevance_dict.keys():
            relevant_docs = relevance_dict[query_id]
            total_retrieved = 0
            total_relevant_retrieved = 0

            for doc in docs:
                total_retrieved += 1
                rank = docs.index(doc) + 1

                if doc in relevant_docs:
                    if total_relevant_retrieved == 0:
                        reciprocal_rank.append(1.0/rank)
                    total_relevant_retrieved += 1
                relevance_flag = 1 if doc in relevant_docs else 0
                precision = float(total_relevant_retrieved)/total_retrieved

                try:
                    precision_dict[query_id][str(rank)] = precision
                except KeyError:
                    precision_dict[query_id] = {str(rank) : precision}

                if rank == 5:
                    precision_at_5.append((query_id,precision))
                if rank == 20:
                    precision_at_20.append((query_id,precision))

                if relevance_flag:
                    average_precision += precision

                recall = float(total_relevant_retrieved)/len(relevant_docs)

                try:
                    recall_dict[query_id][str(rank)] = recall
                except KeyError:
                    recall_dict[query_id] = {str(rank) : recall}

            if total_relevant_retrieved != 0:
                average_precision = average_precision/total_relevant_retrieved
            else:
                average_precision = 0

            average_precision_list.append(average_precision)

    mean_average_precision = sum(precision for precision in average_precision_list)/len(average_precision_list)
    print(mean_average_precision)

    print(precision_at_5)

    print(precision_at_20)

    mean_reciprocal_rank = sum(rank for rank in reciprocal_rank)/len(reciprocal_rank)
    print(mean_reciprocal_rank)

    write_to_file(name,precision_at_5,precision_at_20,mean_reciprocal_rank,
                  mean_average_precision,precision_dict,recall_dict,query_dict)


def write_to_file(name,precision_at_5,precision_at_20,mean_reciprocal_rank,
                  mean_average_precision,precision_dict,recall_dict,query_dict):

    with open(dir + name + "_MAP.csv", "w") as file:
        csv_writer = csv.writer(file)
        csv_writer.writerow([mean_average_precision])
        file.close()

    with open(dir + name + "_MRR.csv", "w") as file:
        csv_writer = csv.writer(file)
        csv_writer.writerow([mean_reciprocal_rank])
        file.close()

    with open(dir + name + "_P@K=5.csv", "w") as file:
        csv_writer = csv.writer(file)
        for entry in precision_at_5:
            csv_writer.writerow((entry[0],entry[1]))
        file.close()

    with open(dir + name + "_P@K=20.csv", "w") as file:
        csv_writer = csv.writer(file)
        for entry in precision_at_20:
            csv_writer.writerow((entry[0], entry[1]))
        file.close()

    with open(dir + name + "_Precision&Recall.csv", "w") as file:
        csv_writer = csv.writer(file)
        for query_id,docs in query_dict.items():
            if query_id in relevance_dict.keys():
                i = 1
                for doc in docs:
                    print(query_id,i)
                    precision_value = precision_dict[query_id][str(i)]
                    recall_value = recall_dict[query_id][str(i)]
                    csv_writer.writerow((query_id,doc,precision_value,recall_value))
                    i += 1
        file.close()

    for query_id,values in precision_dict.items():
        precision_values = list(values.values())
        recall_values = list(recall_dict[query_id].values())

        plt.plot(recall_values,precision_values)
        print(query_id)
    plt.savefig(plots + name + '.png')


def generate_tables():
    calculate_effectiveness(vsm_file,"vsm")
    calculate_effectiveness(bm25_file,"bm25")
    calculate_effectiveness(tfidf_file,"tfidf")
    calculate_effectiveness(lucene_file,"lucene")
    calculate_effectiveness(query_expansion_file,"query_expansion")
    calculate_effectiveness(stopping_file,"stopping")
    calculate_effectiveness(stemming_file,"stemming")
    calculate_effectiveness(query_expansion_with_stopping_file,"query_expansion_with_stopping")

generate_tables()