from dbconnection import db

class user(db.Model):
    __tablename__="tbl_user"
    user_id = db.Column(db.Integer, primary_key=True)
    First_name = db.Column(db.String(200))
    Last_name = db.Column(db.String(200))
    Email = db.Column(db.String(100))
    Phone = db.Column(db.String(15))
    Password = db.Column(db.String(255))
    role_id = db.Column(db.Integer, db.ForeignKey('tbl_role.id'))

class role(db.Model):
    __tablename__ = "tbl_role"
    id = db.Column(db.Integer, primary_key=True)
    role = db.Column(db.String(200))

class auth(db.Model):
    __tablename__ = "tbl_auth"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('tbl_user.user_id'))
    role_id = db.Column(db.Integer, db.ForeignKey('tbl_user.role_id'))
    token = db.Column(db.String(200))
    token_exp = db.Column(db.String(45))
    otp = db.Column(db.Integer)