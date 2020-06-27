from datetime import datetime
from zhuraapp import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    money = db.Column(db.Float, nullable=False, default='1000')
    # delete image after
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    analisis_results = db.relationship('AnalisisResult', backref='creator', lazy=True)
    # thing to properly print this class
    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


# класс для сохранения результатов анализа
class AnalisisResult(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    vk_id = db.Column(db.String(120), nullable=False)
    vk_name = db.Column(db.String(120), nullable=False)
    vk_photo = db.Column(db.String(200), nullable=False, default='img/deactivated_200.png')

    # thing to properly print this class
    def __repr__(self):
        return f"AnalysisResult('{self.id}', '{self.timestamp}', '{self.user_id}', '{self.vk_id}', '{self.vk_name}')"

