"""REST API for listing all available services."""
import flask
import index
import re
from math import sqrt

@index.app.route('/api/v1/hits/', methods=['GET'])
def get_hits():
    """Return a list of hits for the user query."""
    w = flask.request.args.get("w", type=float)
    query = flask.request.args.get("q", type=str).split()

    if w is None or (w < 0 or w > 1):
        response = flask.jsonify(
            message="Bad Request",
            status_code=400,
        )
        flask.abort(response)

    # Clean query
    query = [re.sub(r'[^a-zA-Z0-9]+', '', word) for word in query]
    query = [word for word in query if word not in index.stopwords]

    # Compute query vector
    q_vec = [index.inverted_index_idfs[word] for word in query]
    
    # Find docids of documents containing all query words
    hit_docids = []
    if len(query) > 0:
        hit_docids = [docid for docid in index.inverted_index_docs[query[0]].keys()]
    for word in query:
        hit_docids = list(set(hit_docids) & set([docid for docid in index.inverted_index_docs[word].keys()]))

    # Compute scores for each hit
    scores = []
    for docid in hit_docids:
        d_vec = [(index.inverted_index_idfs[word]*index.inverted_index_docs[word][docid]["occurrences"]) for word in query]

        dot = sum(i[0]*i[1] for i in zip(q_vec, d_vec))
        norm_q = sqrt(sum([x**2 for x in q_vec]))
        norm_d = sqrt(index.inverted_index_docs[word][docid]["norm_squared"])

        tfidf = dot / (norm_q * norm_d)
        pagerank = index.pagerank[docid]

        scores.append(w*pagerank + (1-w)*tfidf)

    hits = list(zip(scores, hit_docids))
    hits.sort()
    hits = [{ "docid": hit[0], "score": hit[1] } for hit in hits]

    context = {
      "hits": hits
    }
    return flask.jsonify(**context)
