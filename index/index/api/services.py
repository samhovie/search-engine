"""REST API for listing all available services."""
import flask
import index


@index.app.route('/api/v1/', methods=['GET'])
def get_services():
    """Return a list of all available REST API services."""
    context = {
      "hits": "/api/v1/hits/",
      "url": "/api/v1/",
    }
    return flask.jsonify(**context)
