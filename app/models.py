from app import db

class BasicInfo(db.Model):
    __tablename__ = 'basic_info'
    page_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    ID = db.Column(db.String(50))
    ALIGN = db.Column(db.String(50))
    SEX = db.Column(db.String(50))
    ALIVE = db.Column(db.String(50))
    YEAR = db.Column(db.String(10))

class Appearance(db.Model):
    __tablename__ = 'appearance'
    id = db.Column(db.Integer, primary_key=True)
    page_id = db.Column(db.Integer, db.ForeignKey('basic_info.page_id'), nullable=False)
    EYE = db.Column(db.String(50))
    HAIR = db.Column(db.String(50))

class OtherInfo(db.Model):
    __tablename__ = 'other_info'
    id = db.Column(db.Integer, primary_key=True)
    page_id = db.Column(db.Integer, db.ForeignKey('basic_info.page_id'), nullable=False)
    GSM = db.Column(db.String(50))
    APPEARANCES = db.Column(db.String(10))
    FIRST_APPEARANCE = db.Column(db.String(50))

class UrlInfo(db.Model):
    __tablename__ = 'url_info'
    id = db.Column(db.Integer, primary_key=True)
    page_id = db.Column(db.Integer, db.ForeignKey('basic_info.page_id'), nullable=False)
    urlslug = db.Column(db.String(200))