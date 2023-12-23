FROM python:3.10

WORKDIR /home/vk_tg_sync

COPY alembic alembic
COPY sync sync
COPY alembic.ini .
COPY main.py .
COPY req.txt .

RUN pip install -r req.txt

CMD [ "python", "main.py" ]