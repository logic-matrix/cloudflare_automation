from dotenv import load_dotenv
from flask import Blueprint, jsonify, render_template
from app.controllers.api_controller import  workers
from app.controllers.users_controller import get_user_name
from CloudFlare import CloudFlare
import os
 

main = Blueprint('main', __name__)

@main.route("/")
def index():
    name = get_user_name()
    return render_template("index.html", name=name)

# Route: Get list of Cloudflare Workers
@main.route('/workers', methods=['GET'])
def get_workers():
    worker = workers
    return jsonify(worker), 200
 

 
