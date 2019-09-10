Nivel 1
Objetivos:
 1.Desarrollar un microservicio en flask que implemente la llamada [GET] /active con una respuesta dummy fija.
 2.Crear una imagen docker que contenga dicho microservicio y publicarla en dockerhub.
Se precedio a realizar el siguiente Procedimiento para crear el API/Micro servicio.
Realizado los siguiente Procedimientos.
Estructura de carpetas:
    ├── Nivel-1
    │   ├── app
    │   │   ├── app.py
    │   │   ├── dummy.py
    │   │   └── requirements.txt
    │   └── Dockerfile
    
   FROM python
COPY app /app
RUN pip install -r /app/requirements.txt
WORKDIR app
CMD ["python", "app.py"]
EXPOSE 5000
app.py
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
    app.run(debug=True, host='0.0.0.0'
   
   dummy_res.py
    dummy_ventas = [{
    "active": True,
    "country": "ni",
    "city": "Leon",
  }
]

requirements
Click==7.0
Flask==1.1.1
Flask-MySQL==1.4.0
Flask-MySQLdb==0.2.0
itsdangerous==1.1.0
Jinja2==2.10.1
MarkupSafe==1.1.1
mysqlclient==1.4.2.post1
PyMySQL==0.9.3
redis==3.2.1
Werkzeug==0.15.5

Nivel 2
Objetivos:
1.Ampliar el microservicio par que implemente la llamada [POST] /active. El estado, la ciudad y el país se deberá almacenar en una base de datos relacional.
2.Modificar el microservicio para que la llamada [GET] /active obtenga sus resultados desde la base de datos.
3.Orquestar el funcionamiento del microservicio con el de la base de datos haciendo uso de docker-compose. La base de datos en concreto es indiferente, pero se recomienda utilizar postgres, mysql o mariadb
4.Crear una imagen docker que contenga dicho microservicio y publicarla en dockerhub.
se precedio a realizar el rchivo Dockerfile utilizando los diferentes procedimientos explicados en clase:Las imágenes de dockerfile son archivos que usa el proceso o procesos que se arrancan en los contenedores.
Estructura de carpetas:
Nivel-2
    │   ├── app
    │   │   ├── app.py
    │   │   ├── __pycache__
    │   │   │   ├── app.cpython-37.pyc
    │   │   │   └── worklog.cpython-37.pyc
    │   │   ├── requirements.txt
    │   │   └── worklog.py
    │   ├── docker-compose.yml
    │   ├── Dockerfile
    │   └── nicaventas
    │       └── schema.sql

docker-compose.yml
version: '3'
services:
  NicaVentas:
    image: galeanom26/nicaventa:N2
    build:
      context: ./Disponibilidad
      dockerfile: Dockerfile
    volumes:
      - ./Disponibilidad/app:/app
    ports:
      - "8000:5000"
    environment:
      - FLASK_DEBUG=1
      - DATABASE_PASSWORD=nicaventaspass
      - DATABASE_NAME=nicaventasdb
      - DATABASE_USER=nicaventasuser
      - DATABASE_HOST=NicaVentas-DB
    command: flask run --host=0.0.0.0
  NicaVentas-DB:
    image: mysql:5
    environment:
      - MYSQL_ROOT_PASSWORD=nv123
      - MYSQL_DATABASE=nicaventasdb
      - MYSQL_USER=nicaventasuser
      - MYSQL_PASSWORD=nicaventaspass
    expose:
      - 3306
    volumes:
      - ./schema.sql:/docker-entrypoint-initdb.d/schema.sql
      
      schema.sql
      CREATE TABLE IF NOT EXISTS location(
    country varchar(2) NOT NULL,
    city varchar(52) NOT NULL,
    active ENUM('True', 'False') NOT NULL,
    PRIMARY KEY (country, city)
) ENGINE=innodb; 

INSERT INTO location (country, city, active) values ('AG', 'San Juan', 'False');
INSERT INTO location (country, city, active) values ('PA', 'Ciudad De Panama', 'False');
INSERT INTO location (country, city, active) values ('PG', 'Puerto De Moresby', 'False');
INSERT INTO location (country, city, active) values ('PK', 'Islamabad', 'False');
INSERT INTO location (country, city, active) values ('PY', 'Asuncion', 'False');
INSERT INTO location (country, city, active) values ('TT', 'Puerto De España', 'False');

DockerFile
FROM python
COPY app /app
RUN pip install -r /app/requirements.txt
WORKDIR app
CMD ["python", "app.py"]
EXPOSE 5000

requirements.txt
Click==7.0
Flask==1.1.1
Flask-MySQL==1.4.0
Flask-MySQLdb==0.2.0
itsdangerous==1.1.0
Jinja2==2.10.1
MarkupSafe==1.1.1
mysqlclient==1.4.2.post1
PyMySQL==0.9.3
redis==3.2.1
Werkzeug==0.15.5

Worklog
class Worklog:

    def __init__(self, dbcon, logger):
        self._dbcon=dbcon
        self._logger=logger

    def save_location(self, **kwargs):
        sql = """
        insert into location 
            (country, city, active) 
            values ('{}','{}','{}')
        """.format(
                kwargs['country'],
                kwargs['city'],
                kwargs['active'])
        cur = self._dbcon.connection.cursor()
        cur.execute(sql)
        self._dbcon.connection.commit()
        cur.close()
        self._logger.info(sql)

    def update_location(self, **kwargs):
        sql = """
        update location set active='{}' where country='{}' and city='{}'; 
        """.format(
                kwargs['active'],
                kwargs['country'],
                kwargs['city'])
        cur = self._dbcon.connection.cursor()
        rv = cur.execute(sql)
        self._dbcon.connection.commit()
        cur.close()
        self._logger.info(sql)
        return rv

    def obtain_location(self, country, city):
        sql = """
        select * from location where country='{}' and city='{}';
        """.format(country, city)
        cur = self._dbcon.connection.cursor()
        cur.execute(sql)
        rv = cur.fetchall()
        cur.close()
        self._logger.info(rv)
        return rv
        
Nivel 3
Objetivos:
1.Modificar el microservicio para que la respuesta de la llamada [GET] /active se haga desde una cache REDIS. La respuesta de este servicio ahora incluirá un campo cache que valdrá miss si la respuesta procede de la base de datos, y hit si la respuesta procede de caché.
2.Modificar el microservicio para que la respuesta de la llamada [POST] /active invalide el posible contenido cacheado en REDIS.
3.Añadir al archivo docker-compose el servicio de redis.
Estrucura de carpeta:
Nivel-3
    │   ├── app
    │   │   ├── app.py
    │   │   ├── requirements.txt
    │   │   └── worklog.py
    │   ├── docker-compose.yml
    │   └── Dockerfile
    
Procedmientos a desarrollar:
docker-compose.yml
ersion: '3'
services:
  nicaventa:
    image: galeanom26/nicaventa:Nivel-3
    build:
      context: ./Disponibilidad
      dockerfile: Dockerfile
    volumes:
      - ./Disponibilidad/app:/app
    ports:
      - "8000:5000"
    environment:
      - FLASK_DEBUG=1
      - DATABASE_PASSWORD=nicaventaspass
      - DATABASE_NAME=nicaventasdb
      - DATABASE_USER=nicaventasuser
      - DATABASE_HOST=NicaVentas-DB
      - REDIS_LOCATION=redis
      - REDIS_PORT=6379
    command: flask run --host=0.0.0.0
  NicaVentas-DB:
    image: mysql:5
    environment:
      - MYSQL_ROOT_PASSWORD=nv123
      - MYSQL_DATABASE=nicaventasdb
      - MYSQL_USER=nicaventasuser
      - MYSQL_PASSWORD=nicaventaspass
    expose:
      - 3306
    volumes:
      - ./schema.sql:/docker-entrypoint-initdb.d/schema.sql
  redis:
    image: redis
    expose:
      - 6379

schema.sql
CREATE TABLE IF NOT EXISTS location(
    country varchar(2) NOT NULL,
    city varchar(52) NOT NULL,
    active ENUM('True', 'False') NOT NULL,
    PRIMARY KEY (country, city)
) ENGINE=innodb;

Dockerfile
FROM python
COPY app /app
RUN pip install -r /app/requirements.txt
WORKDIR app
CMD ["python", "app.py"]
EXPOSE 5000

app.py
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
  
requirements.txt
Click==7.0
Flask==1.1.1
Flask-MySQL==1.4.0
Flask-MySQLdb==0.2.0
itsdangerous==1.1.0
Jinja2==2.10.1
MarkupSafe==1.1.1
mysqlclient==1.4.2.post1
PyMySQL==0.9.3
redis==3.2.1
Werkzeug==0.15.5

Worklog
class Worklog:

    def __init__(self, dbcon, logger):
        self._dbcon=dbcon
        self._logger=logger

    def save_location(self, **kwargs):
        sql = """
        insert into location 
            (country, city, active) 
            values ('{}','{}','{}')
        """.format(
                kwargs['country'],
                kwargs['city'],
                kwargs['active'])
        cur = self._dbcon.connection.cursor()
        cur.execute(sql)
        self._dbcon.connection.commit()
        cur.close()
        self._logger.info(sql)

    def update_location(self, **kwargs):
        sql = """
        update location set active='{}' where country='{}' and city='{}'; 
        """.format(
                kwargs['active'],
                kwargs['country'],
                kwargs['city'])
        cur = self._dbcon.connection.cursor()
        rv = cur.execute(sql)
        self._dbcon.connection.commit()
        cur.close()
        self._logger.info(sql)
        return rv

    def obtain_location(self, country, city):
        sql = """
        select * from location where country='{}' and city='{}';
        """.format(country, city)
        cur = self._dbcon.connection.cursor()
        cur.execute(sql)
        rv = cur.fetchall()
        cur.close()
        self._logger.info(rv)
        return rv
Nivel 4
Objetivos:
1.Evolucionar la arquitectura existente para incluir un micro servicio que proporcione el API [POST] /quote, según lo especificado en el enunciado en Servicio de consulta de condiciones de venta
2.Añadir al archivo docker-compose el nuevo microservicio.
3.Añadir políticas de cacheo de forma que si se solicita [POST] /quote con los mismos parámetros se responda desde la cache de REDIS en lugar de volver a realizar la consultas a OpenWeather y la BBDD. La valided de uno de estos datos cacheados será de 5 min. Con objeto de verificar que la cache funciona, incluir en la respuesta un campo cache como se hizo anteriormente.
Estructura de carpetas:
Nivel-4
        ├── Condiciones
        │   ├── app.py
        │   ├── requirements.txt
        │   └── worklog.py
        ├── Disponibilidad
        │   ├── app.py
        │   ├── requirements.txt
        │   └── worklog.py
        ├── docker-compose.yml
        └── Dockerfile




