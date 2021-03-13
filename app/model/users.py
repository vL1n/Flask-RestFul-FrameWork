from app.model import db


# 用户信息表
class User(db.Model):
    ###
    #orm示例
    ###
    __tablename__ = 'user'
    # 学号
    uid = db.Column(db.Integer, primary_key=True, comment='学号')
    # 上网账号
    network_username = db.Column(db.VARCHAR(20), nullable=False, comment='上网账号')
    # 上网密码
    network_password = db.Column(db.VARCHAR(20), nullable=False, comment='上网密码')
    # 校园卡查询密码
    card_password = db.Column(db.Integer, nullable=False, comment='校园卡查询密码')
    # 图书馆借阅密码
    library_password = db.Column(db.Integer, nullable=False, comment='图书馆借阅密码')
    # 教务处查询密码
    jwc_password = db.Column(db.VARCHAR(20), nullable=False, comment='教务处查询密码')
