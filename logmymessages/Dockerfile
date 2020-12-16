FROM python:3.6

WORKDIR /opt/logmymessages

# Installing dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# copy project
COPY . .

CMD ["gunicorn", "--bind", "0.0.0.0:8080", "app:app"]

HEALTHCHECK --interval=30s --timeout=3s CMD curl -f http://localhost:8080/health-check || exit 1