"""Insta485 package initializer."""
from pathlib import Path
import flask

# app is a single object used by all the code modules in this package
app = flask.Flask(__name__)  # pylint: disable=invalid-name

# Load search files
INDEX_ROOT = Path(__file__).resolve().parent
inverted_index_file = (INDEX_ROOT/"inverted_index.txt").open(mode="r")
pagerank_file = (INDEX_ROOT/"pagerank.out").open(mode="r")
stopwords_file = (INDEX_ROOT/"stopwords.txt").open(mode="r")

# Create usable data structures from files
inverted_index_idfs = {}
inverted_index_docs = {}
for line in inverted_index_file:
    vals = line.strip().split()
    inverted_index_idfs[vals[0]] = float(vals[1])
    inverted_index_docs[vals[0]] = {}
    for i in range(2, len(vals), 3):
        inverted_index_docs[vals[0]][int(vals[i])] = {
            "occurrences": int(vals[i+1]),
            "norm_squared": float(vals[i+2]),
        }

pagerank = {}
for line in pagerank_file:
    pair = line.strip().split(",")
    pagerank[int(pair[0])] = float(pair[1])

stopwords = []
for line in stopwords_file:
    stopwords.append(line.strip())

# Tell our app about views and model.  This is dangerously close to a
# circular import, which is naughty, but Flask was designed that way.
# (Reference http://flask.pocoo.org/docs/patterns/packages/)  We're
# going to tell pylint and pycodestyle to ignore this coding style violation.
import index.api    # noqa: E402  pylint: disable=wrong-import-position
