from flask import Blueprint, request, jsonify, render_template
from helpers import token_required
from models import db, User, Soju, soju_schema, sojus_schema

api = Blueprint('api',__name__, url_prefix='/api')

@api.route('/getdata')
def getdata():
    return {'yee': 'haw'}

@api.route('/sojus', methods = ['POST'])
@token_required
def create_soju(current_user_token):
    name = request.json['name']
    style = request.json['style']
    flavor = request.json['flavor']
    user_token = current_user_token.token

    print(f'BIG TESTER: {current_user_token.token}')

    soju = Soju(name, style, flavor, user_token = user_token)

    db.session.add(soju)
    db.session.commit()

    response = soju_schema.dump(soju)
    return jsonify(response)

@api.route('/sojus', methods = ['GET'])
@token_required
def get_soju(current_user_token):
    a_user = current_user_token.token
    sojus = Soju.query.filter_by(user_token = a_user).all()
    response = sojus_schema.dump(sojus)
    return jsonify(response)

@api.route('/sojus/<id>', methods = ['GET'])
@token_required
def get_soju_id(current_user_token, id):
    fan = current_user_token.token
    if fan == current_user_token.token:
        soju = Soju.query.get(id)
        response = soju_schema.dump(soju)
        return jsonify(response)
    else:
        return jsonify({"message":"Valid Token Required"}), 401

@api.route('/sojus/<id>', methods = ['POST', 'PUT'])
@token_required
def update_soju(current_user_token, id):
    soju = Soju.query.get(id)
    soju.name = request.json['name']
    soju.style = request.json['style']
    soju.flavor = request.json['flavor']
    soju.user_token = current_user_token.token

    db.session.commit()
    response = soju_schema.dump(soju)
    return jsonify(response)

@api.route('/sojus/<id>', methods = ['DELETE'])
@token_required
def delete_soju(current_user_token, id):
    soju = Soju.query.get(id)
    db.session.delete(soju)
    db.session.commit()
    response = soju_schema.dump(soju)
    return jsonify(response)