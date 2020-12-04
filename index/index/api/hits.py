"""REST API for listing all available services."""
from math import sqrt
import re
import flask
import index


@index.app.route('/api/v1/hits/', methods=['GET'])
def get_hits():
    """Return a list of hits for the user query."""
    weight = flask.request.args.get("w", type=float)
    query = flask.request.args.get("q", type=str).split()

    if weight is None or (weight < 0 or weight > 1):
        response = flask.jsonify(
            message="Bad Request",
            status_code=400,
        )
        flask.abort(response)

    # Clean query
    query = [re.sub(r'[^a-zA-Z0-9]+', '', word) for word in query]
    query = [word for word in query if word not in index.stopwords]

    # Short-circuit if any query word is not in index
    for word in query:
        if word not in index.inverted_index_idfs:
            context = {
                "hits": []
            }
            return flask.jsonify(**context)

    # Compute query vector
    q_vec = [index.inverted_index_idfs[word] for word in query]

    # Find docids of documents containing all query words
    hit_docids = []
    if len(query) > 0:
        hit_docids = index.inverted_index_docs[query[0]].keys()
    for word in query:
        hit_docids = list(
            set(hit_docids) & set(index.inverted_index_docs[word].keys())
        )

    # Compute scores for each hit
    scores = []
    for docid in hit_docids:
        d_vec = [(index.inverted_index_idfs[word] *
                 index.inverted_index_docs[word][docid]["occurrences"])
                 for word in query]
        dot = sum(i[0]*i[1] for i in zip(q_vec, d_vec))
        norm_q = sqrt(sum([x**2 for x in q_vec]))
        norm_d = sqrt(index.inverted_index_docs[word][docid]["norm_squared"])
        tfidf = dot / (norm_q * norm_d)
        scores.append(weight * index.pagerank[docid] + (1 - weight) * tfidf)

    hits = list(zip(hit_docids, scores))
    hits.sort(key=lambda tup: tup[0], reverse=False)
    hits.sort(key=lambda tup: tup[1], reverse=True)
    hits = [{"docid": hit[0], "score": hit[1]} for hit in hits]

    context = {
      "hits": hits
    }
    return flask.jsonify(**context)
