#!/usr/bin/env python3
"""Map 3."""

import json
import sys

for line in sys.stdin:
    doc_id, norm, words = json.loads(line)
    for word, idf, count in words:
        print(f"{word}\t{json.dumps([idf, doc_id, count, norm])}")
