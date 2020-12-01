import os.path

from marshmallow import Schema, fields

from frank_proctor.app import app
from frank_proctor.article_generator import ArticleGenerator
from frank_proctor import responses
from frank_proctor.constants import MODEL_DIR

from .utils import validate_request


class LoadModelRequestSchema(Schema):
    model = fields.String(required=True)


@app.route('/load-model', methods=['POST'])
@validate_request(LoadModelRequestSchema)
def load_model(args):
    model = args.get('model')
    model_path = os.path.join(MODEL_DIR, model)

    if not os.path.isdir(model_path):
        return responses.model_not_found()

    ArticleGenerator.get().load_model(model_path)

    return responses.success()
