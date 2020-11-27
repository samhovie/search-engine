#!/usr/bin/env python3
"""Map 1."""

import csv
import json
import re
import sys

def extract_words(row, stop_words):
    """Extract all words in row."""
    words = row[1].split() + row[2].split()
    words = [re.sub(r"[^a-zA-Z0-9]+", "", word) for word in words]
    words = [word.lower() for word in words if word != ""]
    words = [word for word in words if word not in stop_words]
    words_dict = {}
    for word in words:
        if word not in words_dict:
            words_dict[word] = 0
        words_dict[word] += 1
    return [(word, words_dict[word]) for word in words_dict]


stop_words = None
with open("stopwords.txt", "r") as stop_words_file:
    stop_words = set(stop_words_file.readlines())

csv.field_size_limit(sys.maxsize)
for row in csv.reader(sys.stdin):
    doc_id = row[0]
    words = extract_words(row, stop_words)
    for word, count in words:
        print(f"{word}\t{json.dumps([doc_id, count])}")
