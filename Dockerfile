FROM python:3.11-buster

WORKDIR /app
RUN useradd 9000
RUN pip install --upgrade pip && pip install requests && pip install beautifulsoup4 && pip install lxml
COPY secadv.py /app/
USER 9000
CMD ["python3", "/app/secadv.py"]
