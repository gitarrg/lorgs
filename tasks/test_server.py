"""Quick test server to help developer the Cloud Functions.
(functions_framework was weird)

"""
# IMPORT THIRD PARTY LIBRARIES
import flask

# IMPORT LOCAL LIBRARIES
import main

# Flask
app = flask.Flask(__name__)


@app.route("/load_spec_rankings")
def load_spec_rankings():
    return main.load_spec_rankings(flask.request)


app.run(host="localhost", port=8000, debug=True)
