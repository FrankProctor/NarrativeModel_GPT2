from frank_proctor.app import app
from frank_proctor import responses


@app.route('/ping')
def ping():
    return responses.success('pong')
