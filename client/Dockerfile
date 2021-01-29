FROM python:latest
WORKDIR /usr/local/bin
COPY . .
RUN pip3 install -r requirements.debug.txt
EXPOSE 6667/tcp
EXPOSE 42069/tcp
CMD ["python", "client.py"]



