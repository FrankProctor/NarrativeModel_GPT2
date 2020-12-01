import logging
import os
import os.path
import frank_proctor.endpoints  # noqa

from waitress import serve
from frank_proctor.app import app
from frank_proctor.article_generator import ArticleGenerator
from frank_proctor.constants import MODEL_DIR, DEFAULT_MODEL


def main():
    logging.basicConfig(level=os.getenv('LOG_LEVEL', 'INFO').upper())

    ArticleGenerator.get().load_model(os.path.join(MODEL_DIR, DEFAULT_MODEL))
    serve(app, listen='*:8080')


if __name__ == '__main__':
    main()
