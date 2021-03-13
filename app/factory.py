import os
import yaml
import logging
import logging.config
from flask import Flask, request, Blueprint
from flask_restful import Resource, Api
from flask_cors import CORS
from flask_swagger import swagger
from app.router import router
from flask_migrate import Migrate
from app.model import db
from app.utils.core import JSONEncoder
# db migrate用
from app.model.users import *


def create_app(config_name, config_path=None):
    app = Flask(__name__)

    if not config_path:
        pwd = os.getcwd()
        config_path = os.path.join(pwd, 'config/main_config.yaml')
    if not config_name:
        config_name = 'PRODUCTION'

    # 获取配置
    conf = read_yaml(config_name, config_path)
    app.config.update(conf)

    # 读取msg配置
    with open(app.config['RESPONSE_MESSAGE'], 'r', encoding='utf-8') as f:
        msg = yaml.safe_load(f.read())
        app.config.update(msg)

    # 注册接口到蓝图
    register_api(app=app, routers=router)

    # 返回json格式转换
    app.json_encoder = JSONEncoder

    # 数据库初始化
    migrate = Migrate(app, db)
    db.init_app(app)

    # 日志文件目录
    if not os.path.exists(app.config['LOGGING_PATH']):
        os.mkdir(app.config['LOGGING_PATH'])

    # 日志设置
    with open(app.config['LOGGING_CONFIG_PATH'], 'r', encoding='utf-8') as f:
        dict_conf = yaml.safe_load(f.read())
    logging.config.dictConfig(dict_conf)

    return app


def read_yaml(config_name, config_path):
    """
    :param config_name: 配置名称
    :param config_path: 配置路径，db.init_app(app)默认为： ../config/main_config.yaml
    :return:
    """
    if config_name and config_path:
        with open(config_path, 'r', encoding='utf-8') as f:
            conf = yaml.safe_load(f.read())  # yaml.load(f.read())
        if config_name in conf.keys():
            return conf[config_name.upper()]
        else:
            raise KeyError('未找到对应的配置信息')
    else:
        raise ValueError('请输入正确的配置名称或配置文件路径')


def register_api(app, routers):
    for router_api in routers:
        if isinstance(router_api, Blueprint):
            app.register_blueprint(router_api)
        else:
            try:
                endpoint = router_api.__name__
                view_func = router_api.as_view(endpoint)
                # url默认为类名小写
                url = '/{}/'.format(router_api.__name__.lower())
                if 'GET' in router_api.__methods__:
                    app.add_url_rule(url, defaults={'key': None}, view_func=view_func, methods=['GET', ])
                    app.add_url_rule('{}<string:key>'.format(url), view_func=view_func, methods=['GET', ])
                if 'POST' in router_api.__methods__:
                    app.add_url_rule(url, view_func=view_func, methods=['POST', ])
                if 'PUT' in router_api.__methods__:
                    app.add_url_rule('{}<string:key>'.format(url), view_func=view_func, methods=['PUT', ])
                if 'DELETE' in router_api.__methods__:
                    app.add_url_rule('{}<string:key>'.format(url), view_func=view_func, methods=['DELETE', ])
            except Exception as e:
                raise ValueError(e)
