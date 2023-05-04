FROM python:3.10
WORKDIR /REST_API
COPY ./requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "app.py"]
