FROM python:3.11
WORKDIR /REST_API
COPY ./requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "app.py"]
