# Use lightweight Python image
FROM python:3.9-slim

WORKDIR /app

# Copy everything
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Required by Google Cloud Run
EXPOSE 8080

# Launch app with production WSGI server
CMD ["gunicorn", "-w", "2", "-b", "0.0.0.0:8080", "app:app"]
