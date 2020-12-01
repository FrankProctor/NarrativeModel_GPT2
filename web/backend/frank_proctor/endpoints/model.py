from frank_proctor.app import app
from frank_proctor import responses
from frank_proctor.article_generator import ArticleGenerator


@app.route('/model')
def model():
    return responses.success(ArticleGenerator.get().model_name)
