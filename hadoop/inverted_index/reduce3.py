#!/usr/bin/env python3
"""Reduce 3."""

import json
import sys

words = {}

for line in sys.stdin:
    word, data = line.split("\t", 1)
    idf, doc_id, count, norm = json.loads(data)

    if word not in words:
        words[word] = {
            "idf": idf,
            "docs": []
        }

    words[word]["docs"].append([doc_id, str(count), str(norm)])

for word in words:
    doc_data = " ".join([" ".join(data) for data in words[word]["docs"]])
    print(f"{word} {words[word]['idf']} {doc_data}")
