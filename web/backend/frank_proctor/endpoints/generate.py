from marshmallow import Schema, fields

from frank_proctor.app import app
from frank_proctor import responses
from frank_proctor.article_generator import (
    ArticleGenerator,
    ModelNotFound,
    ModelNotLoaded,
)

from .utils import validate_request


class GenerateRequestSchema(Schema):
    prompt_text = fields.String(required=True)
    output_length = fields.Integer(missing=50)
    num_output = fields.Integer(missing=1)
    trim_ending = fields.Boolean(missing=True)


@app.route('/generate', methods=['POST'])
@validate_request(GenerateRequestSchema)
def generate(args):

    prompt_text = args.get('prompt_text')
    output_length = args.get('output_length')
    num_output = args.get('num_output')
    should_trim_ending = args.get('trim_ending')

    try:
        results = ArticleGenerator.get().generate(
            prompt_text,
            output_length=output_length,
            num_return_sequences=num_output,
            should_trim_ending=should_trim_ending)
        return responses.success(results)
    except ModelNotFound:
        return responses.model_not_found()
    except ModelNotLoaded:
        return responses.model_not_loaded()
