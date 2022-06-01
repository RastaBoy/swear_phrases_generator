from quart import Blueprint

webgui = Blueprint('webgui', __name__)

from .routes import *