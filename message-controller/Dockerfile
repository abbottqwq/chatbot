FROM python:3.9-alpine
WORKDIR /app
COPY ./requirements.txt .
RUN pip install -r requirements.txt
COPY . .
ENV DEBUG=0
ENTRYPOINT [ "python" ]
CMD ["app.py"]