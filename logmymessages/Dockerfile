FROM python:3.6

WORKDIR /opt/logmymessages

# copy project
COPY . .

# Installing dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt


CMD ["gunicorn", "--bind", "0.0.0.0:8080", "app:app"]

HEALTHCHECK --interval=30s --timeout=3s CMD curl -f http://localhost:8080/health-check || exit 1