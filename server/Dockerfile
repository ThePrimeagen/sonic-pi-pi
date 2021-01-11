FROM python:latest
WORKDIR /usr/local/bin
COPY . .
RUN pip3 install -r requirements.txt
EXPOSE 42069/tcp
CMD ["python", "server.py"]
