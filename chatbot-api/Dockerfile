FROM python:3.8
RUN pip install numpy
RUN pip install tensorflow
WORKDIR /app
COPY ./requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "app.py"]