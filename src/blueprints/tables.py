from hashlib import algorithms_available
import json
from lib2to3.pgen2 import token
import secrets
from flask import Blueprint
from src.database.models import User, Colors
from src.database import session
from flask import Flask, request, jsonify, make_response

from src.database.models.Color import mixColors
from .auth import token_required
from datetime import datetime, timedelta
from functools import wraps
from sqlalchemy import func
from sqlalchemy.sql import text

import random
table_blueprint = Blueprint("table", __name__)

@table_blueprint.route('/table', methods=["GET"])
@token_required
def get_table(current_user):
    colors = session.query(Colors).all()
    to_return = {}
    index = 0
    for color in colors:
        c = color.toJson();
        to_return[index] = c
        index +=1
    return  to_return, 200

@table_blueprint.route('/count_favorite_colors', methods=["GET"])
@token_required
def get_number_favorite_color(current_user):
    colors = session.query(Colors.favorite_color, 
        func.count(Colors.favorite_color).label("nColor")).group_by(Colors.favorite_color).order_by("nColor").limit(10).all()
    to_return = json.dumps( [dict(ix) for ix in colors] )
    return  to_return, 200

@table_blueprint.route('/count_hated_colors', methods=["GET"])
@token_required
def get_number_hated_color(current_user):
    colors = session.query(Colors.hated_color, 
        func.count(Colors.hated_color).label("nColor")).group_by(Colors.hated_color).order_by("nColor").limit(10).all()
    to_return = json.dumps( [dict(ix) for ix in colors] )
    return  to_return, 200


@table_blueprint.route('/get_all_users', methods=["GET"])
@token_required
def get_all_user_colors(current_user):
    #colors = session.query(Colors, User).join(User.public_id).all()
    query = text("select(favorite_color, hated_color, random_color, lucky_color, name) from colors, usertable where public_id = person")
    results = session.execute(query).fetchall()
    to_return = []
    i=0
    for result in results:
        i+=1
        row = result[0]
        row = row[1:-1]
        items = row.split(',')
        row_item=[]
        for item in items:
            row_item.append(item)
        to_return.append({
            "id":i,
            "favorite_color":row_item[0], "hated_color":row_item[1], "random_color":row_item[2], "lucky_color":row_item[3], "name":row_item[4]
        })
    return {"data":to_return}, 200

@table_blueprint.route('/color', methods=["POST"])
@token_required
def set_color(current_user):
    data = request.json
    if not "favorite_color" or "hated color" in data:
        return make_response("missing data", status=400)
    luckyC = mixColors(data["favorite_color"],data["hated_color"])
    query = session.query(Colors).where(
        Colors.person == current_user.public_id).first()
    setattr(query, "favorite_color",data["favorite_color"])
    setattr(query, "hated_color", data["hated_color"])
    setattr(query, "lucky_color", luckyC)
    session.commit()
    return make_response("done",200)