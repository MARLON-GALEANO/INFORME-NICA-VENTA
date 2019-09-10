Nivel 1
Objetivos:
 1.Desarrollar un microservicio en flask que implemente la llamada [GET] /active con una respuesta dummy fija.
 2.Crear una imagen docker que contenga dicho microservicio y publicarla en dockerhub.
Se precedio a realizar el siguiente Procedimiento para crear el API/Micro servicio.
Realizado la siguiente configuraciones.
Servicios_VentasNica
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
