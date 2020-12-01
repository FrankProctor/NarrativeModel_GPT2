from flask import jsonify, make_response


def success(data=None):
    resp = {'status': 'ok'}
    if data is not None:
        if isinstance(data, dict):
            resp = {
                **resp,
                **data
            }
        else:
            resp['result'] = data
    return make_response(jsonify(resp))


def failure(status, code, reason):
    if isinstance(reason, str):
        reason = {
            'message': reason
        }

    return make_response(jsonify({
        'status': 'failed',
        'error': {
            'code': code,
            **reason
        }
    }), status)


def invalid_arguments(info):
    return failure(400, 1001, {
        'message': 'Invalid arguments',
        'info': info
    })


def model_not_found():
    return failure(404, 2001, "Model not found")


def model_not_loaded():
    return failure(404, 2002, "Model not loaded")
