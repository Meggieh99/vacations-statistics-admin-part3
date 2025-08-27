FROM python:3.11-slim

WORKDIR /app

COPY initial_data.json .
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY manage.py .                       
COPY stats_backend ./stats_backend      
COPY vacations ./vacations              
COPY stats_api ./stats_api             

CMD ["python", "manage.py", "runserver", "0.0.0.0:9000"]
