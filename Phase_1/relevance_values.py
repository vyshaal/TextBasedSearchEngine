import re
import pickle

relevance_values_file_path = "../given_files/cacm.rel"
relevance_dict = {}


def read_file():
    with open(relevance_values_file_path) as file:
        for line in file:
            entry = line.split(" ")
            value = work_around(str(entry[2]))
            try:
                relevance_dict[entry[0]] += "," + value
            except KeyError:
                relevance_dict[entry[0]] = value

    pickle.dump(relevance_dict, open("relevance_dict.p", "wb"))
#    print(relevance_dict)


def work_around(s):
    while len(s) < 9:
        s = s.replace('-', '-0')
    return s

read_file()

