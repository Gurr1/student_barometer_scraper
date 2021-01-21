FROM python:3.9
WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
## THIS RUNS IN DEVELOPMENT MODE AND SHOULD REALLY NOT.
ENV FLASK_APP=backend.py
CMD ["python", "backend.py"]