FROM python:3.12

WORKDIR app/

COPY *.py ./
COPY py-part/ ./py-part
COPY static/ ./
COPY templates/ ./
COPY settings.txt ./
COPY requirements.txt ./

RUN pip install -r requirements.txt

EXPOSE 8080

ENTRYPOINT ["python"] 

CMD ["webserver.py"]
