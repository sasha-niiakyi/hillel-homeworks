FROM python:3.10

ENV HOME=/home/bank
ENV DB_HOST="host.docker.internal"

RUN mkdir -p $HOME

COPY . $HOME

WORKDIR $HOME/bank

RUN pip install --upgrade pip
RUN pip install pipenv
RUN pipenv install

EXPOSE 8000

CMD pipenv run python manage.py migrate && pipenv run python manage.py runserver 0.0.0.0:8000