"""REST API for listing all available services."""
import flask
import index


@index.app.route('/api/v1/hits/', methods=['GET'])
def get_hits():
    """Return a list of hits for the user query."""
    w = flask.request.args.get("w", default=0.5, type=float)
    query = flask.request.args.get("q", default="", type=str)

    context = {
      "hits": [
          {
              "docid": 0,
              "score": 0.0
          }
      ]
    }
    return flask.jsonify(**context)
