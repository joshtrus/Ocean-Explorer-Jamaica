from flask import Flask, jsonify, render_template
import boto3

app = Flask(__name__)

dynamodb = boto3.resource('dynamodb', region_name='us-east-2')
shop_table = dynamodb.Table('dive_shop_details')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dive-shops', methods=['GET'])
def get_dive_shops():
    response = shop_table.scan()
    dive_shops = response.get('Items', []) 
    return jsonify(dive_shops) 

if __name__ == '__main__':
    app.run(debug=True)

