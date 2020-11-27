#!/usr/bin/env python3
"""Reduce 2."""

import json
import sys

docs = {}

for line in sys.stdin:
    doc_id, data = line.split("\t", 1)
    word, idf, count = json.loads(data)

    if doc_id not in docs:
        docs[doc_id] = []

    docs[doc_id].append((word, idf, count))

for doc_id in docs:
    norm = 0
    for word, idf, count in docs[doc_id]:
        norm += count ** 2 * idf ** 2
    print(json.dumps([doc_id, norm, docs[doc_id]]))
