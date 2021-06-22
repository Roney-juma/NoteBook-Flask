from flask import Blueprint

main = Blueprint('blog',__name__)

from . import views,forms