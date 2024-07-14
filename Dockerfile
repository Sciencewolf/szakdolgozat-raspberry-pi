FROM python:3.12

WORKDIR app/

COPY *.py ./
COPY py-part/ ./py-part
COPY static/ ./
COPY templates/ ./
COPY stuff/ ./stuff
COPY requirements.txt ./

RUN pip install -r requirements.txt

EXPOSE 8080

CMD ["python", "webserver.py"]
