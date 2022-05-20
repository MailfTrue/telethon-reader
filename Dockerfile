FROM python:3.10.4

COPY ./requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . code
WORKDIR code

ENTRYPOINT [ "python", "main.py" ]
