#!/usr/bin/python3
"""
Blueprint setup for the API v1
"""

from flask import Blueprint

# Create a Blueprint instance for the API
app_views = Blueprint("app_views", __name__, url_prefix="/api/v1")

# Wildcard import of everything in `api.v1.views.index`
from api.v1.views.index import *
from api.v1.views.states import *
from api.v1.views.cities import *
