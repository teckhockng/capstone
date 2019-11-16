FROM tiangolo/uwsgi-nginx-flask:python3.7

COPY ./app /app
WORKDIR /app
RUN pip install -r requirements.txt
EXPOSE 5000
CMD python ./main.py
