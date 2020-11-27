#!/usr/bin/env python3
"""Reduce 0."""

import sys

count = 0
for _ in sys.stdin:
    count += 1

with open("total_document_count.txt", "w") as f:
    f.write(f"{count}\n")
