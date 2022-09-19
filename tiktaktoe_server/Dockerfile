FROM python
WORKDIR /server/TikTakToe
RUN apt-get update && apt-get -y upgrade
RUN curl -sSL https://install.python-poetry.org | python3 -
COPY . /server/TikTakToe
RUN ~/.local/share/pypoetry/venv/bin/poetry export -f requirements.txt > /server/TikTakToe/requirements.txt
RUN pip install -r /server/TikTakToe/requirements.txt
EXPOSE 8090
ENTRYPOINT ["sh", "entrypoint.sh"]