from .extensions import db
from datetime import datetime, timezone

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    is_admin = db.Column(db.Boolean, default=False, nullable=False)
    profile = db.relationship('CitizenProfile', uselist=False, back_populates='user', cascade='all, delete-orphan')

class CitizenProfile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), unique=True, nullable=False)
    age = db.Column(db.Integer)
    state = db.Column(db.String(100))
    occupation = db.Column(db.String(100))
    annual_income = db.Column(db.Float)
    interests = db.Column(db.Text, default='')
    user = db.relationship('User', back_populates='profile')
    def as_dict(self):
        return {k:getattr(self,k) for k in ('age','state','occupation','annual_income','interests')}

class Scheme(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(100), nullable=False)
    official_url = db.Column(db.String(1000), nullable=False)
    source_verified_at = db.Column(db.Date, nullable=True)
    rules = db.Column(db.JSON, nullable=False, default=dict)
    rule_version = db.Column(db.Integer, nullable=False, default=1)
    active = db.Column(db.Boolean, nullable=False, default=False)
    def as_dict(self):
        return {"id":self.id,"name":self.name,"description":self.description,"category":self.category,"official_url":self.official_url,"source_verified_at":self.source_verified_at.isoformat() if self.source_verified_at else None,"rule_version":self.rule_version,"rules":self.rules,"active":self.active}

class SavedScheme(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    scheme_id = db.Column(db.Integer, db.ForeignKey('scheme.id'), nullable=False)
    __table_args__ = (db.UniqueConstraint('user_id','scheme_id'),)
