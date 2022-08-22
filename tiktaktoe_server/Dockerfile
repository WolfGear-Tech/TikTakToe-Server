FROM python
WORKDIR /server/TikTakToe
RUN apt-get update && apt-get -y upgrade
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -
COPY . /server/TikTakToe
RUN $HOME/.poetry/bin/poetry export -f requirements.txt > /server/TikTakToe/requirements.txt
RUN pip install -r /server/TikTakToe/requirements.txt
EXPOSE 8090
ENTRYPOINT ["sh", "entrypoint.sh"]