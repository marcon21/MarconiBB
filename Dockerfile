FROM python:3.7
ADD ./flask/requirements.txt /setup/requirements.txt
WORKDIR /setup
RUN pip install -r requirements.txt
CMD python app.py