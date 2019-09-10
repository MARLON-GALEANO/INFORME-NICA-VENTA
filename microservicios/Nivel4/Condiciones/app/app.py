from flask import Flask, jsonify, request, escape
from flask_mysqldb import MySQL
import os
import ftfy
import json
import requests
import redis
from worklog import Worklog
app = Flask(__name__)
app.config['MYSQL_HOST'] = os.environ['DATABASE_HOST']
app.config['MYSQL_USER'] = os.environ['DATABASE_USER']
app.config['MYSQL_PASSWORD'] = os.environ['DATABASE_PASSWORD']
app.config['MYSQL_DB'] = os.environ['DATABASE_NAME']
mysql = MySQL(app)

redis_cli = redis.Redis(host=os.environ['REDIS_LOCATION'], port=os.environ['REDIS_PORT'], charset="utf-8", decode_responses=True)
@app.route('/price/<sku>')
def get_product_price(sku):
    try:
        wl = Worklog(mysql, app.logger)
        result = wl.get_price(escape(sku))
        price = float(result[0][0])
        description = str(result[0][1])

        response = {
            "price": float(price),
            "sku": escape(sku),
            "description": description
        }
        return jsonify(response)
    except:
        return jsonify({"message":"Datos no Asociados"})

@app.route('/quote', methods=['POST'])
def post_location():
    try:
        payload = request.get_json()
        country = payload['country']
        city = payload['city']
        sku = payload['sku']

        key = str(country) + '-' + str(city) + '-' + str(sku)

        info_cache = redis_cli.get(escape(key))

        if info_cache:
            cache = "hit"
            js = json.loads(info_cache)
            price = float(js['base_price'])
            description = str(js['description'])
            variation= float(js['variation'])
        else:
            cache = "miss"
            r = requests.get('https://api.openweathermap.org/data/2.5/weather?q='+str(city)+','+str(country)+'&appid=3225ae99d4c4cb46be4a2be004226918')
            weather = r.json()
            wl = Worklog(mysql, app.logger)
            result = wl.obtain_condition(country, city, sku, weather['weather'][0]['id'])

            if(result):
                variation = float(result[0][0])
                description = result[0][1]
                price = float(result[0][2])
            else:
                result2 = wl.obtain_product(**payload)
                description = result2[0][0]
                price = float(result2[0][1])
                variation = float(1.0)
            redis_cli.set(str(key), str('{"base_price": '+str(price)+', "description":"'+str(description)+'", "variation": '+str(variation)+'}'))
            redis_cli.expire(str(key),300)

        return jsonify({
            "sku": payload['sku'],
            "description": description,
            "country": payload['country'],
            "city": payload['city'],
            "base_price": price,
            "variation": variation,
            "redis_cache": cache})
    except:
        return jsonify({'message':' Datos no  Asociados'})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

