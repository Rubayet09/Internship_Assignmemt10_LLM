FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install -r requirements.txt

# Copy project files
COPY . ./app

# Create directories for data
RUN mkdir -p hotel_images

# Expose port
EXPOSE 8000

# Run the scraper
# CMD ["python", "-m", "projectscrape.main"]