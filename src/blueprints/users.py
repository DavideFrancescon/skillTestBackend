from flask import Blueprint
from src.database.models import User, Colors, mixColors
from src.database import session
from flask import request, make_response
from .auth import token_required
from src.database.models.Color import mixColors

users_blueprint = Blueprint("users", __name__)


@users_blueprint.route('/user', methods=["PUT"])
@token_required
def update_user(current_user):
    data = request.json
    query = session.query(Colors).where(
        Colors.person == current_user.public_id).first()
    setattr(current_user, 'name', data["name"])
    setattr(query, 'favorite_color', data["favorite_color"])
    lucky_color = mixColors(data["favorite_color"], data["hated_color"])
    setattr(query, 'lucky_color', lucky_color)
    setattr(query, 'hated_color', data["hated_color"])
    session.commit()
    query = "select * from usertable JOIN colors on person = public_id where public_id = '%s'" % current_user.public_id
    user = session.execute(query).first()
    user_return = {}
    for item in user.keys():
        user_return[item] = user[item]
    return user_return, 200


@users_blueprint.route('/change_random_color', methods=["PUT"])
@token_required
def update_lucky_color(current_user):
    data = request.json
    query = session.query(Colors).where(
        Colors.person == current_user.public_id).first()
    setattr(query, 'random_color', data["random_color"])
    session.commit()
    return {}, 200


@users_blueprint.route('/color', methods=["POST"])
@token_required
def set_color(current_user):
    data = request.json
    if not "favorite_color" or "hated color" in data:
        return make_response("missing data", status=400)
    luckyC = mixColors(data["favorite_color"], data["hated_color"])
    query = session.query(Colors).where(
        Colors.person == current_user.public_id).first()
    setattr(query, "favorite_color", data["favorite_color"])
    setattr(query, "hated_color", data["hated_color"])
    setattr(query, "lucky_color", luckyC)
    session.commit()
    return make_response("done", 200)
