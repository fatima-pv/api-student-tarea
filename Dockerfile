
FROM python:3.11-slim

WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    APP_PORT=3000 \
    DB_PATH=/data/students.sqlite

# Install runtime dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app
COPY . .

# Prepare DB directory and initialize schema
RUN mkdir -p /data && python db.py

EXPOSE 3000
# Use gunicorn for production
CMD ["gunicorn", "-w", "2", "-b", "0.0.0.0:3000", "app:app"]
