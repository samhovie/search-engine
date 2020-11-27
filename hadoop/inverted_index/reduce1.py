#!/usr/bin/env python3
"""Reduce 1."""

import itertools
import json
import math
import sys

def get_data(line):
    word, data = line.split("\t", 1)
    doc_id, count = json.loads(data)
    return (word, doc_id, count)


num_docs = None
with open("total_document_count.txt", "r") as count_file:
    num_docs = int(count_file.read())

for word, group in itertools.groupby(map(get_data, sys.stdin), key=lambda data: data[0]):
    group = list(map(lambda data: (data[1], data[2]), group))
    idf = math.log10(num_docs / len(group))
    print(json.dumps([word, idf, group]))
