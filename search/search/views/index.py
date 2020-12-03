import flask
import search
import requests

@search.app.route('/', methods=['GET', 'POST'])
def show_index():
    # Connect to database
    connection = search.model.get_db()

    # Handle search requests
    search_results = []
    user_searched = False
    weight = None
    query = None
    if 'q' in flask.request.args and 'w' in flask.request.args:
        user_searched = True
        # Look in the Flask form for w and q
        weight = flask.request.args.get('w')
        query = flask.request.args.get("q")

        # Call REST API with w and q
        # Results are already sorted by score, so we can just get the first 10
        # results (at most) here.
        try:
            response = requests.get(search.app.config["INDEX_API_URL"], params={
                'w': weight,
                'q': query,
            }).json()["hits"][0:10]
        except requests.exceptions.ConnectionError:
            return flask.abort(500, "Index server not found")

        # Go through the docids in the JSON and query database for title, summary matching docid
        for hit in response:
            doc = connection.execute(
                "SELECT title, summary FROM Documents "
                "WHERE docid = ?;",
                (hit["docid"],)
            ).fetchone()
            assert(doc is not None)
            search_results.append(doc)

    context = {
        'user_searched': user_searched,
        'search_results': search_results,
        'weight': weight,
        'query': query,
    }
    return flask.render_template('index.html', **context)