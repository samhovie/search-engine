#!/usr/bin/env python3
"""Reduce 3."""

import itertools
import json
import sys

def get_data(line):
    word, data = line.split("\t", 1)
    idf, doc_id, count, norm = json.loads(data)
    return (word, idf, doc_id, count, norm)


for word, group in itertools.groupby(map(get_data, sys.stdin), key=lambda data: data[0]):
    group = map(lambda data: (data[1], data[2], data[3], data[4]), group)
    header_printed = False
    for idf, doc_id, count, norm in group:
        if not header_printed:
            print(f"{word} {idf}", end="")
            header_printed = True
        print(f" {doc_id} {count} {norm}", end="")
    print()
