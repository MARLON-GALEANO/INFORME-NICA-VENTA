from flask import Flask, jsonify, request, escape
from flask_mysqldb import MySQL
import os
import redis
from worklog import Worklog
app = Flask(__name__)
app.config['MYSQL_HOST'] = os.environ['DATABASE_HOST']
app.config['MYSQL_USER'] = os.environ['DATABASE_USER']
app.config['MYSQL_PASSWORD'] = os.environ['DATABASE_PASSWORD']
app.config['MYSQL_DB'] = os.environ['DATABASE_NAME']
mysql = MySQL(app)


redis_cli = redis.Redis(host=os.environ['REDIS_LOCATION'], port=os.environ['REDIS_PORT'], charset="utf-8", decode_responses=True)
@app.route('/active')
def get_location():
    try:
        country = request.args.get('country')
        city = request.args.get('city')
        key = str(country) + '-' + str(city)

        active = redis_cli.get(escape(key))

        if active:
            cache = "hit"
            country = request.args.get('country')
            city = request.args.get('city')
            return jsonify({"active": eval(active), "country":country, "city":city, "redis_cache":cache})
        else:
            cache = "miss"
            country = request.args.get('country')
            city = request.args.get('city')
            wl = Worklog(mysql, app.logger)
            result = wl.obtain_location(escape(country), escape(city))

            if result[0][2].find("True") != -1:
                active = True
            else:
                active = False

            redis_cli.set(str(key),escape(active))
            return jsonify({"active": active, "country":result[0][0], "city":result[0][1], "redis_cache":cache})
    except:
        return jsonify({"message":" Datos no Asociados"})


@app.route('/active', methods=['PUT'])
def put_location():
    try:
        payload = request.get_json()
        country = payload['country']
        city = payload['city']
        key = str(country) + '-' + str(city)
        auth = request.headers.get("Authorization", None)

        if not auth:
            return jsonify({"message":"No se ha enviado el Token"})
        elif auth != "Bearer 2234hj234h2kkjjh42kjj2b20asd6918":
            return jsonify({"message":"Token no Autorizado!"})
        else:
            wl = Worklog(mysql, app.logger)
            result = wl.update_location(**payload)

            if result == 1:
                redis_cli.delete(escape(key))
                return jsonify({'result':'Ok', 'update': payload})
            else:
                return jsonify({'result':'Fail', 'message': 'Actualizar Informacion'})
    except:
        return jsonify({'result':'ERROR', 'message':'Error, verifique  request'})


@app.route('/active', methods=['POST'])
def post_location():
    try:
        payload = request.get_json()
        wl = Worklog(mysql, app.logger)
        wl.save_location(**payload)
        return jsonify({'result':'Ok', 'Insert': payload})
    except:
        return jsonify({'result':'ERROR', 'message':'Error, verifique  request'})


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

