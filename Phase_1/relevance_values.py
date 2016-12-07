import re
import pickle

relevance_values_file_path = "../given_files/cacm.rel"
relevance_values = {}


def read_file():
    with open(relevance_values_file_path) as file:
        for line in file:
            entry = line.split(" ")
            try:
                value = relevance_values[entry[0]] + "," + str(entry[2])
            except KeyError:
                value = str(entry[2])
            relevance_values[entry[0]] =value

    pickle.dump(relevance_values, open("relevance_values.p", "wb"))
    print(relevance_values)

read_file()

