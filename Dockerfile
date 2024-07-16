FROM python:3.11

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY ./GCNet ./GCNet
COPY ./checkpoint ./checkpoint
COPY ./endpoint ./endpoint

EXPOSE 4000  
WORKDIR /app/endpoint
CMD ["uvicorn", "infer:app", "--host", "0.0.0.0", "--port", "4000"]