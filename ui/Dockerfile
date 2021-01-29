FROM python:latest
WORKDIR /usr/local/bin
COPY . .
RUN pip3 install -r requirements.txt
EXPOSE 6969/tcp
CMD ["python", "ui.py"]
