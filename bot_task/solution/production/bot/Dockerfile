FROM python:buster

COPY bot/ bot/

COPY bot.config ./


RUN pip3 install -r /bot/requirements.txt

WORKDIR ./bot

ENTRYPOINT ["python"]

CMD ["bot.py"]