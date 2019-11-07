FROM python:3.5-alpine

LABEL mainteiner="Luiz Antonio <luizgj@iprianga.com.br>"

RUN pip install --upgrade pip

RUN adduser -D worker
USER worker
WORKDIR /home/worker

ENV PATH="/home/worker/.local/bin:${PATH}"

COPY --chown=worker:worker requirements.txt requirements.txt

RUN pip install --user -r requirements.txt --trusted-host nexus3-cideveloper.ipp.openshift.locawebcorp.com.br

COPY --chown=worker:worker . .

ADD ./*.py ./
ADD ./resources/ ./resources/

RUN python3 -m pytest tests/*.py -v

ENTRYPOINT ["sh", "-c", "gunicorn --worker-tmp-dir /dev/shm --bind 0.0.0.0:8000 --reuse-port wsgi:application"]