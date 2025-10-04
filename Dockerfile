FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app


# Mysql Client
RUN apt-get update && apt-get install -y default-mysql-client \
    && rm -rf /var/lib/apt/lists/*




# System dependencies for bcrypt compilation
RUN apt-get update && \
    apt-get install -y build-essential libffi-dev libssl-dev && \
    rm -rf /var/lib/apt/lists/*

# Copy requirements and install pinned packages
COPY requirements.txt .

# Force correct versions of passlib + bcrypt
RUN pip install --upgrade pip && \
    pip install --no-cache-dir --force-reinstall passlib[bcrypt]==1.7.4 bcrypt==3.2.0 && \
    pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app ./app

EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
