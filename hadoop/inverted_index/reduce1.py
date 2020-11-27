#!/usr/bin/env python3
"""Reduce 1."""

import json
import math
import sys


words_dict = {}

for line in sys.stdin:
    word, data = line.split("\t", 1)
    doc_id, count = json.loads(data)

    if word not in words_dict:
        words_dict[word] = []

    words_dict[word].append((doc_id, count))

num_docs = None
with open("total_document_count.txt", "r") as count_file:
    num_docs = int(count_file.read())

for word in words_dict:
    idf = math.log10(num_docs / len(words_dict[word]))
    print(json.dumps([word, idf, words_dict[word]]))
