
# flask imports
import datetime
from py_compile import main
from socket import create_connection
from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base  
from blueprints import auth
from dotenv import load_dotenv

load_dotenv()

import os
sql_string = os.environ.get("sql_string")


db = create_engine(sql_string)
base = declarative_base()
Session = sessionmaker(db)  
session = Session()
