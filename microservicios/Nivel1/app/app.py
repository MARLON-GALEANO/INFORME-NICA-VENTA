from flask import Flask, jsonify, request
import dummy_res
import os
app = Flask(__name__)
#RUTA DUMMY RESPONSE
@app.route('/active')
def get_dummy():
    return jsonify(dummy_res.dummy_ventas)

#PUERTO POR DEFECTO 5000
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

