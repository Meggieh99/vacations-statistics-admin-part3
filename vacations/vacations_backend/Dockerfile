FROM python:3.11-slim

WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy manage.py
COPY manage.py .

# Copy the vacations folder
COPY vacations ./vacations

# הוספת נתיב מודולים לפייתון
ENV PYTHONPATH="${PYTHONPATH}:/app/vacations"

# Expose port
EXPOSE 8000

# Run server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
