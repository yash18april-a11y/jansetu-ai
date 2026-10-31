import os
from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.exc import IntegrityError
from .extensions import db, jwt
from .models import User, CitizenProfile, Scheme, SavedScheme
from .engine import evaluate, rank_schemes

def create_app(test_config=None):
    app = Flask(__name__)
    app.config.update(SQLALCHEMY_DATABASE_URI=os.getenv(
    'DATABASE_URL',
    'mysql+pymysql://jansetu:jansetu@localhost:3306/jansetu'
).replace('postgres://', 'postgresql://', 1), SQLALCHEMY_TRACK_MODIFICATIONS=False, JWT_SECRET_KEY=os.getenv('JWT_SECRET_KEY',''))
    if test_config: app.config.update(test_config)
    if not app.config['JWT_SECRET_KEY']: raise RuntimeError('Set JWT_SECRET_KEY to a strong random secret')
    db.init_app(app); jwt.init_app(app)
    CORS(app, origins=os.getenv('FRONTEND_ORIGIN','http://localhost:5173').split(','), supports_credentials=False)

    @app.get('/api/health')
    def health(): return jsonify(status='ok',service='JanSetu AI')

    @app.post('/api/auth/register')
    def register():
        body=request.get_json(silent=True) or {}
        email=str(body.get('email','')).strip().lower(); password=body.get('password','')
        if not email or '@' not in email or not isinstance(password,str) or len(password)<10:
            return jsonify(error='Valid email and password of at least 10 characters required'),400
        user=User(email=email,password_hash=generate_password_hash(password))
        db.session.add(user)
        try: db.session.flush();db.session.add(CitizenProfile(user_id=user.id));db.session.commit()
        except IntegrityError: db.session.rollback();return jsonify(error='Email already registered'),409
        return jsonify(message='Account created'),201

    @app.post('/api/auth/login')
    def login():
        body=request.get_json(silent=True) or {};user=User.query.filter_by(email=str(body.get('email','')).strip().lower()).first()
        if not user or not check_password_hash(user.password_hash,body.get('password','')):return jsonify(error='Invalid credentials'),401
        return jsonify(access_token=create_access_token(identity=str(user.id)))

    @app.route('/api/profile',methods=['GET','PUT'])
    @jwt_required()
    def profile():
        u=db.session.get(User,int(get_jwt_identity()))
        if not u:return jsonify(error='User not found'),404
        if request.method=='GET':return jsonify(u.profile.as_dict())
        body=request.get_json(silent=True) or {}
        allowed={'age','state','occupation','annual_income','interests'}
        if any(k not in allowed for k in body):return jsonify(error='Unknown profile field'),400
        try:
            if 'age' in body and body['age'] is not None and not 0<=int(body['age'])<=120:raise ValueError()
            if 'annual_income' in body and body['annual_income'] is not None and float(body['annual_income'])<0:raise ValueError()
            for key,value in body.items():
                if key in {'state','occupation','interests'} and value is not None and (not isinstance(value,str) or len(value)>500):raise ValueError()
                if key=='age' and value is not None:value=int(value)
                if key=='annual_income' and value is not None:value=float(value)
                setattr(u.profile,key,value)
        except (ValueError,TypeError):return jsonify(error='Invalid profile values'),400
        db.session.commit();return jsonify(u.profile.as_dict())

    @app.get('/api/schemes')
    def schemes():return jsonify([s.as_dict() for s in Scheme.query.filter_by(active=True).order_by(Scheme.name).all()])

    @app.get('/api/schemes/<int:scheme_id>')
    def scheme_detail(scheme_id):
        s=db.session.get(Scheme,scheme_id)
        if not s or not s.active:return jsonify(error='Not found'),404
        return jsonify(s.as_dict())

    @app.post('/api/recommendations')
    @jwt_required()
    def recommendations():
        u=db.session.get(User,int(get_jwt_identity()));body=request.get_json(silent=True) or {}
        if not u:return jsonify(error='User not found'),404
        q=str(body.get('query') or u.profile.interests or u.profile.occupation or '')[:500]
        items=rank_schemes(q,[s.as_dict() for s in Scheme.query.filter_by(active=True).all()])
        for item in items:item['eligibility']=evaluate(u.profile.as_dict(),item['rules'])
        return jsonify(items)

    @app.post('/api/schemes/<int:scheme_id>/eligibility')
    @jwt_required()
    def eligibility(scheme_id):
        u=db.session.get(User,int(get_jwt_identity()));s=db.session.get(Scheme,scheme_id)
        if not u or not s or not s.active:return jsonify(error='Not found'),404
        return jsonify(evaluate(u.profile.as_dict(),s.rules),official_url=s.official_url,source_verified_at=s.source_verified_at.isoformat() if s.source_verified_at else None)

    @app.route('/api/saved',methods=['GET','POST'])
    @jwt_required()
    def saved():
        uid=int(get_jwt_identity())
        if request.method=='GET':
            ids=[x.scheme_id for x in SavedScheme.query.filter_by(user_id=uid).all()]
            return jsonify([s.as_dict() for s in Scheme.query.filter(Scheme.id.in_(ids),Scheme.active.is_(True)).all()])
        body=request.get_json(silent=True) or {}
        try:sid=int(body.get('scheme_id'))
        except (ValueError,TypeError):return jsonify(error='Valid scheme_id required'),400
        if not db.session.get(Scheme,sid):return jsonify(error='Scheme not found'),404
        if not SavedScheme.query.filter_by(user_id=uid,scheme_id=sid).first():
            db.session.add(SavedScheme(user_id=uid,scheme_id=sid));db.session.commit()
        return jsonify(message='Saved'),201

    @app.errorhandler(404)
    def missing(_):return jsonify(error='Not found'),404
    return app
