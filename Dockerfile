FROM python:alpine
ARG UID=1000
ARG GID=1000
RUN addgroup snakeeater -g $GID
RUN adduser snakeeater -u $UID -G snakeeater --disabled-password
USER snakeeater
COPY . .
RUN pip3 install --no-cache-dir --upgrade pip
RUN pip3 install -r requirements.txt
#ENTRYPOINT ["python", "-m", "mnamer"]
#CMD ["-rb", "/data/anime", "/data/tvseries", "/data/movies", "/data/kids"]
#python -m mnamer -rb /data/anime /data/tvseries /data/movies /data/kids
CMD python -m ./snakeeater.py