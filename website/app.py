from flask import Flask, jsonify, render_template, request
import boto3
from concurrent.futures import ThreadPoolExecutor




app = Flask(__name__)

dynamodb = boto3.resource('dynamodb', region_name='us-east-2')
shop_table = dynamodb.Table('dive_shop_details')

def filter_shops(dive_shops, search_query, filter_type):
    filtered_shops = dive_shops
    if search_query:
        filtered_shops = [shop for shop in dive_shops if search_query in shop.get('address', '').lower()]
    if filter_type:
        filtered_shops = [shop for shop in dive_shops if shop.get('activity', '').lower() == filter_type.lower()]

    return filtered_shops

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/shops')
def index():
    return render_template('index.html')


@app.route('/dive-shops', methods=['GET'])
def get_dive_shops():
    search_query = request.args.get('search', '').lower()
    filter_type = request.args.get('filter', '')

    response = shop_table.scan()
    dive_shops = response.get('Items', [])  

    with ThreadPoolExecutor() as executor:
        future = executor.submit(filter_shops, dive_shops, search_query, filter_type)
        dive_shops = future.result()

    
    return jsonify(dive_shops)  

if __name__ == '__main__':
    app.run(debug=True)

