from functools import wraps


class GlobalMiddleware(object):
    """
    全局中间件
    """

    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        # print('before')
        middle = self.app(environ, start_response)
        # print('after')
        return middle


GlobalMiddleware = GlobalMiddleware


def login_required(func):
    """
    自定义中间件
    :param func:
    :return:
    """

    @wraps(func)
    def decorated_function(*args, **kwargs):
        # print('hello, middleware')
        return func(*args, **kwargs)

    return decorated_function


def token_check(func):
    """
    自定义中间件
    :param func:
    :return:
    """

    @wraps(func)
    def d_function(*args, **kwargs):
        # print('hello, token_check middleware')
        return func(*args, **kwargs)

    return d_function
