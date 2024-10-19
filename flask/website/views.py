from flask import Blueprint

views = Blueprint('views', __name__)
 

@views.route('/')
def home():
    return "<h1>Test</h1>"

@views.route('/dive-sites')
def sites():
    return "<h1>Test</h1>"

@views.route('/dive-shops')
def shops():
    return "<h1>Test</h1>"