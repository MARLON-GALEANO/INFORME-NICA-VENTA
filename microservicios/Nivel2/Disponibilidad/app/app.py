from flask import Flask, jsonify, request, escape
from flask_mysqldb import MySQL
import os
from worklog import Worklog
app = Flask(__name__)
app.config['MYSQL_HOST'] = os.environ['DATABASE_HOST']
app.config['MYSQL_USER'] = os.environ['DATABASE_USER']
app.config['MYSQL_PASSWORD'] = os.environ['DATABASE_PASSWORD']
app.config['MYSQL_DB'] = os.environ['DATABASE_NAME']
mysql = MySQL(app)

@app.route('/active')
def get_location():
    try:
        country = request.args.get('country')
        city = request.args.get('city')
        wl = Worklog(mysql, app.logger)
        result = wl.obtain_location(escape(country), escape(city))

        if result[0][2].find("True") != -1:
            active = True
        else:
            active = False

        return jsonify({"active": active, "country":result[0][0], "city":result[0][1]})
    except:
        return jsonify({"message":"No existen datos Asociados"})

@app.route('/active', methods=['PUT'])
def put_location():
    try:
        payload = request.get_json()
        auth = request.headers.get("Authorization", None)

        if not auth:
            return jsonify({"message":"No se ha enviado el Token"})
        elif auth != "Bearer 2234hj234h2kkjjh42kjj2b20asd6918":
            return jsonify({"message":"Token no Autorizado!"})
        else:
            wl = Worklog(mysql, app.logger)
            result = wl.update_location(**payload)
            if result == 1:
                return jsonify({'result':'Ok', 'update': payload})
            else:
                return jsonify({'result':'Fail', 'message': 'No se detecto ningun cambio al Actualizar'})
    except:
        return jsonify({'result':'ERROR', 'message':'Ha ocurrido un error, verifique su request'})

@app.route('/active', methods=['POST'])
def post_location():
    try:
        payload = request.get_json()
        wl = Worklog(mysql, app.logger)
        wl.save_location(**payload)
        return jsonify({'result':'Ok', 'Insert': payload})
    except:
        return jsonify({'result':'ERROR', 'message':'Ha ocurrido un error, verifique su request'})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

