from flask import Blueprint, render_template
from app.controllers.users_controller import get_user_name
 

main = Blueprint('main', __name__)

@main.route("/")
def index():
    name = get_user_name()
    return render_template("index.html", name=name)
