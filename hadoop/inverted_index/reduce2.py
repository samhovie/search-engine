#!/usr/bin/env python3
"""Reduce 2."""

import itertools
import json
import sys

def get_data(line):
    doc_id, data = line.split("\t", 1)
    word, idf, count = json.loads(data)
    return (doc_id, word, idf, count)


for doc_id, group in itertools.groupby(map(get_data, sys.stdin), key=lambda data: data[0]):
    norm = 0
    group = list(map(lambda data: (data[1], data[2], data[3]), group))
    for word, idf, count in group:
        norm += count ** 2 * idf ** 2
    print(json.dumps([doc_id, norm, group]))
