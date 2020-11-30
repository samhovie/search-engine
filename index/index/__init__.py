"""Insta485 package initializer."""
from pathlib import Path

# Load search files
inverted_index_file = Path("./inverted_index.txt").open(mode="r")
pagerank_file = Path("./pagerank.out").open(mode="r")
stopwords_file = Path("./stopwords.txt").open(mode="r")

# Create usable data structures from files
inverted_index_idfs = {}
inverted_index_docs = {}
for line in inverted_index_file:
    vals = line.split()
    inverted_index_idfs[vals[0]] = vals[1]
    inverted_index_docs[vals[0]] = {}
    for i in range(start=2, stop=len(vals) step=3):
        inverted_index_docs[vals[0]][vals[i]] = {
            "occurrences": vals[i+1],
            "norm_factor": vals[i+2],
        }

pagerank = {}
for line in pagerank_file:
    pair = line.split(",")
    pagerank[pair[0]] = pair[1] 

stopwords = []
for line in stopwords_file:
    stopwords.append(line)

# Tell our app about views and model.  This is dangerously close to a
# circular import, which is naughty, but Flask was designed that way.
# (Reference http://flask.pocoo.org/docs/patterns/packages/)  We're
# going to tell pylint and pycodestyle to ignore this coding style violation.
import index.api    # noqa: E402  pylint: disable=wrong-import-position
