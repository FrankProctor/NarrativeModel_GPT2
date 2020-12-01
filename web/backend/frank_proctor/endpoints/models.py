import os

from frank_proctor.app import app
from frank_proctor import responses
from frank_proctor import constants


@app.route('/models')
def models():

    models = [
        x.name
        for x in os.scandir(constants.MODEL_DIR) if x.is_dir()
    ]

    return responses.success(models)
