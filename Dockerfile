FROM python:3.10
WORKDIR /code
RUN apt-get update && apt-get -y upgrade
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -
COPY . .
RUN $HOME/.poetry/bin/poetry export --dev -f requirements.txt > requirements.txt
RUN pip install -r requirements.txt
EXPOSE 8090
CMD ["sh", "entrypoint.sh"]