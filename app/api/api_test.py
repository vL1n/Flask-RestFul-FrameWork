from flask import Blueprint, jsonify
from app.middleware.middlewares import login_required
from app.utils.code import ResponseCode
from app.utils.response import ResMsg

bp = Blueprint("test", __name__, url_prefix='/')


@bp.route("/unifiedResponse", methods=["GET"])
@login_required
def test_response():
    """
    测试统一返回消息
    :return:
    """
    # 初始化返回obj
    res = ResMsg()
    # 返回数据（字典格式）
    test_dict = dict(name="zhang", age=18)
    # 更新返回内容
    # 除了可以更新data外，还能更新msg 例如 res.update(code=ResponseCode.Success, msg="example")
    # code 在引入的code文件中选
    res.update(code=ResponseCode.Success, data=test_dict)
    return jsonify(res.data)
