
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
#sql_string = os.environ.get("sql_string")
sql_string = "postgres://jfkvizzofidnbc:a031b17174e6d6c49e6420c68d184ce4fee9f4031fdddf70ebdb8fc6fe7b2e2a@ec2-50-19-255-190.compute-1.amazonaws.com:5432/ddda7ph7cnuaps"

db = create_engine(sql_string)
base = declarative_base()
Session = sessionmaker(db)  
session = Session()
