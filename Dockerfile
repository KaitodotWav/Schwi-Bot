FROM metabase/metabase
FROM python
RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app
COPY . .
EXPOSE 3000
CMD ["Schwi.py"]
ENTRYPOINT ["python"]
