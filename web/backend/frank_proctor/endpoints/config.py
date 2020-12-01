from marshmallow import Schema, fields
from marshmallow.validate import Range

from frank_proctor.app import app
from frank_proctor.article_generator import (
    ArticleGenerator,
    ArticleGeneratorConfig,
)
from frank_proctor import responses

from .utils import validate_request

import logging

logger = logging.getLogger(__name__)


class ConfigRequestSchema(Schema):
    temperature = fields.Float(validate=Range(min=0))
    k = fields.Integer(validate=Range(min=1))
    p = fields.Float(validate=Range(min=0, max=1))
    repetition_penalty = fields.Float(validate=Range(min=1))


@app.route('/config', methods=['POST'])
@validate_request(ConfigRequestSchema)
def config(args):

    old_config = ArticleGenerator.get().config

    ArticleGenerator.get().config = ArticleGeneratorConfig(**{
        field: args.get(field, getattr(old_config, field))
        for field in old_config._fields
    })

    logger.info(ArticleGenerator.get().config.temperature)

    return responses.success()
