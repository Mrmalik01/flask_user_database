FROM python:3.6
FROM kennethreitz/pipenv as build
WORKDIR /usr/src/app
COPY Pipfile .
RUN pip install --upgrade pip
RUN pip install pipenv 
RUN pipenv install &&  pipenv lock -r > requirements.txt
RUN  pip install --no-cache-dir -r requirements.txt
COPY . .
CMD python3 app.py

