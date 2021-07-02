FROM python:3

COPY cogs /usr/local/cogs

ADD Schwi.py / cogs

RUN pip install -r ../requirements.txt

CMD python -u Schwi.py
