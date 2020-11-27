#!/usr/bin/env python3
"""Map 2."""

import json
import sys

for line in sys.stdin:
    word, idf, docs = json.loads(line)
    for doc_id, count in docs:
        print(f"{doc_id}\t{json.dumps([word, idf, count])}")

