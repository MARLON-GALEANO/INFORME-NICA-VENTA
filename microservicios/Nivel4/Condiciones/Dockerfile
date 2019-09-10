FROM python
COPY app /app
RUN pip install -r /app/requirements.txt
RUN pip install requests
RUN pip install ftfy
WORKDIR app
CMD ["python", "app.py"]
EXPOSE 5000


